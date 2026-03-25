#!/usr/bin/env python3
import math
import time
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

import requests


class SpeedtestLiteError(Exception):
    pass


class SpeedtestLite:
    def __init__(self, secure=True, timeout=10):
        self.secure = secure
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/146.0.0.0 Safari/537.36"
            }
        )

        self.client = {}
        self.servers = []
        self.best = {}
        self.ping = None

    def _scheme_url(self, url: str) -> str:
        if url.startswith("://"):
            return f'{"https" if self.secure else "http"}{url}'
        return url

    def _get(self, url: str, **kwargs):
        return self.session.get(self._scheme_url(url), timeout=self.timeout, **kwargs)

    def get_config(self):
        response = self._get("://www.speedtest.net/speedtest-config.php")
        response.raise_for_status()

        try:
            root = ET.fromstring(response.content)
            client = root.find("client")
            if client is None:
                raise SpeedtestLiteError("Missing client info in config response")

            self.client = {
                "ip": client.attrib.get("ip"),
                "isp": client.attrib.get("isp"),
                "lat": float(client.attrib.get("lat", 0)),
                "lon": float(client.attrib.get("lon", 0)),
            }
        except Exception as exc:
            raise SpeedtestLiteError(f"Failed to parse config: {exc}") from exc

    def get_servers(self):
        urls = [
            "://www.speedtest.net/speedtest-servers-static.php",
            "://www.speedtest.net/speedtest-servers.php",
            "http://c.speedtest.net/speedtest-servers-static.php",
            "http://c.speedtest.net/speedtest-servers.php",
        ]

        last_error = None

        for url in urls:
            try:
                response = self._get(url)
                response.raise_for_status()

                root = ET.fromstring(response.content)
                servers = []

                for elem in root.iter("server"):
                    attrib = elem.attrib
                    try:
                        servers.append(
                            {
                                "id": attrib.get("id"),
                                "name": attrib.get("name"),
                                "sponsor": attrib.get("sponsor"),
                                "country": attrib.get("country"),
                                "host": attrib.get("host"),
                                "url": attrib.get("url"),
                                "lat": float(attrib.get("lat", 0)),
                                "lon": float(attrib.get("lon", 0)),
                            }
                        )
                    except Exception:
                        continue

                if servers:
                    self.servers = servers
                    return

            except Exception as exc:
                last_error = exc

        raise SpeedtestLiteError(f"Failed to retrieve server list: {last_error}")

    @staticmethod
    def _distance_km(lat1, lon1, lat2, lon2):
        radius = 6371.0

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radius * c

    def get_closest_servers(self, limit=20):
        if not self.client:
            self.get_config()
        if not self.servers:
            self.get_servers()

        lat1 = self.client["lat"]
        lon1 = self.client["lon"]

        ranked = []
        for server in self.servers:
            try:
                d = self._distance_km(lat1, lon1, server["lat"], server["lon"])
                server = dict(server)
                server["d"] = d
                ranked.append(server)
            except Exception:
                continue

        ranked.sort(key=lambda s: s["d"])
        return ranked[:limit]

    def _latency_url(self, server):
        base = server["url"].rsplit("/", 1)[0]
        stamp = int(time.time() * 1000)
        return f"{base}/latency.txt?x={stamp}"

    def _measure_server_latency(self, server, attempts=3):
        values = []

        for i in range(attempts):
            url = f"{self._latency_url(server)}.{i}"
            try:
                start = time.perf_counter()
                response = self.session.get(url, timeout=3)
                elapsed_ms = (time.perf_counter() - start) * 1000

                if response.status_code == 200 and response.text.strip().startswith(
                    "test=test"
                ):
                    values.append(elapsed_ms)
                else:
                    values.append(3600_000.0)
            except Exception:
                values.append(3600_000.0)

        if not values:
            return None

        avg = round(sum(values) / len(values), 3)
        if avg >= 3600_000.0:
            return None
        return avg

    def get_best_server(self):
        candidates = self.get_closest_servers(limit=25)

        best_server = None
        best_ping = None

        for server in candidates:
            latency = self._measure_server_latency(server, attempts=3)
            if latency is None:
                continue

            if best_ping is None or latency < best_ping:
                best_ping = latency
                best_server = dict(server)
                best_server["latency"] = latency

        if not best_server:
            raise SpeedtestLiteError("No server reachable")

        self.best = best_server
        self.ping = best_ping
        return best_server

    def run(self):
        self.get_config()
        self.get_servers()
        self.get_best_server()

        return {
            "isp": self.client.get("isp"),
            "ip": self.client.get("ip"),
            "server": self.best.get("name"),
            "sponsor": self.best.get("sponsor"),
            "ping": self.ping,
            "distance_km": round(self.best.get("d", 0), 2),
            "server_id": self.best.get("id"),
        }


if __name__ == "__main__":
    st = SpeedtestLite(secure=True)
    result = st.run()

    print(f"ISP: {result['isp']} ({result['ip']})")
    print(
        f"Best Server: {result['sponsor']} - {result['server']} "
        f"[{result['distance_km']} km]"
    )
    print(f"Ping: {result['ping']} ms")
