import datetime as dt
import json
from dataclasses import dataclass
from typing import Optional

from django.conf import settings


def load_flags() -> tuple[dict[str, str], dict[str, str]]:
    ru_flags: dict[str, str]
    en_flags: dict[str, str]
    with open(settings.FLAGS_DIR / "ru_flags.json", "r") as file:
        ru_flags = json.load(file)
    with open(settings.FLAGS_DIR / "en_flags.json", "r") as file:
        en_flags = json.load(file)
    return ru_flags, en_flags


RU_FLAGS, EN_FLAGS = load_flags()


@dataclass
class Location:
    name: str
    region: str
    country: str
    localtime: str
    flag: str
    url: str

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Location":
        country = data.get("country")
        flag = EN_FLAGS.get(country)
        if flag is None:
            flag = RU_FLAGS.get(country)
        return cls(
            name=data.get("name"),
            country=country,
            region=data.get("region"),
            localtime=data.get("localtime"),
            url=data.get("url"),
            flag=flag,
        )

    def to_dict(self):
        return {
            "name": self.name,
            "country": self.country,
            "region": self.region,
            "url": self.url,
            "flag": self.flag,
        }


@dataclass
class Condition:
    text: str
    icon_url: str

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Condition":
        return cls(
            text=data.get("text"),
            icon_url=data.get("icon"),
        )


@dataclass
class Weather:
    condition: Optional[Condition]
    temp_c: float
    wind_kph: float
    feelslike_c: float
    humidity: int
    last_updated: dt.datetime

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Weather":
        return cls(
            condition=Condition.from_dict(data.get("condition")),
            temp_c=data.get("temp_c"),
            wind_kph=data.get("wind_kph"),
            feelslike_c=data.get("feelslike_c"),
            humidity=data.get("humidity"),
            last_updated=dt.datetime.fromisoformat(data.get("last_updated")),
        )


@dataclass
class Hour:
    date: dt.datetime
    temp_c: float
    wind_kph: float
    humidity: int
    condition: Condition

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Hour":
        return cls(
            date=dt.datetime.fromisoformat(data.get("time")),
            temp_c=data.get("temp_c"),
            wind_kph=data.get("wind_kph"),
            humidity=data.get("humidity"),
            condition=Condition.from_dict(data.get("condition")),
        )


@dataclass
class Forecast:
    hours: list[Hour]

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Forecast":
        hours = []
        now_timestamp = (
            dt.datetime.now().replace(minute=0, second=0, microsecond=0).timestamp()
        )
        for day_data in data.get("forecastday", []):
            for hour_data in day_data.get("hour", []):
                if (
                    timestamp := hour_data.get("time_epoch")
                ) is None or timestamp < now_timestamp:
                    continue
                hours.append(Hour.from_dict(hour_data))
        return cls(hours=hours)
