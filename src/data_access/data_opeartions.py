import pandas as pd
from PIL import Image
from io import BytesIO
import numpy as np
from abc import ABC, abstractmethod
from datetime import (datetime,
                    timedelta)
from typing import (List,
                    Tuple,
                    Union)


class DataOperations(ABC):
    _heart_rate: Union[List, None] = None
    _data: Union[List, None] = None

    @property
    @abstractmethod
    def data(self): ...

    @data.setter
    @abstractmethod
    def data(self): ...

    def is_data_none_wrapper(func):
        def __is_data_none(self, *args, **kwargs) -> Union[None, NameError]:
            if self.data is None:
                raise NameError(f'data not found. You must set the data before calling the {func.__name__} function')
            return func(self, *args, **kwargs)
        return __is_data_none

    def is_heart_rate_none_wrapper(func):
        def __is_heart_rate_none(self, *args, **kwargs) -> Union[None, NameError]:
            if self.heart_rate is None:
                raise NameError(f'heart_rate data not found. You must call the get_heart_rate function before calling the {func.__name__} function')
            return func(self, *args, **kwargs)
        return __is_heart_rate_none

    @property
    @is_data_none_wrapper
    def heart_rate(self) -> List:
        # sourcery skip: inline-immediately-returned-variable, list-comprehension
        self._heart_rate = []
        for d in self.data:
            if d['type'] == 7:
                self._heart_rate.append(
                    {
                        'rate': float(d['samplePoints'][0]['value']),
                        'time': (datetime.fromtimestamp(
                                    int(str(d['samplePoints'][0]['endTime'])[:10])
                            ) + timedelta(
                                    hours = int(self.data[0]['timeZone'][1:].replace('0', ''))
                                )
                        )
                    }
                )
        return self._heart_rate

    @is_heart_rate_none_wrapper
    def get_heart_rate_for_all_days_as_axis(self) -> Tuple:
        heart_rate = pd.DataFrame(self._heart_rate)
        return (
            list (
                map(
                    lambda t: t.strftime("%d-%m-%Y %X"),
                    heart_rate['time']
                )
            ),
            heart_rate['rate']
        )

    @is_heart_rate_none_wrapper
    def get_average_heart_rate_for_days_as_axis(self) -> Tuple:
        heart_rate_grouped = pd.DataFrame(
            list(
                map(
                    lambda t: {'rate': t['rate'], 'date': t['time'].strftime("%d-%m-%Y")}, self._heart_rate
                )
            )
        ).groupby('date', sort=False).mean()['rate']

        return (heart_rate_grouped.keys(), heart_rate_grouped.values)

    @is_heart_rate_none_wrapper
    def get_heart_rate_for_one_day(self, day) -> Tuple:
        heart_rate = pd.DataFrame(
            list(
                filter(
                    lambda t: t['time'].strftime("%d-%m-%Y") == day, self._heart_rate
                )
            )
        )

        return (
            list (
                map(
                    lambda t: t.strftime("%d-%m-%Y %X"),
                    heart_rate['time']
                )
            ),
            heart_rate['rate']
        )

    def get_averages_of_heart_rates(self, y: pd.Series, average_number: int) -> Tuple:
        heart_rate2 = []
        rates = list(y)

        for i in range(0, len(rates), average_number):
            t = rates[i:i + average_number]
            heart_rate2.append(sum(t) / len(t))

        return (range(len(heart_rate2)), heart_rate2)

    @classmethod
    def __array_to_bytes_image(cls, img_array: np.array) -> bytes:
        buf = BytesIO()
        Image.fromarray(img_array, 'RGB').save(buf, format="PNG")
        return buf.getvalue()

    @staticmethod
    def get_heart_rate_as_img(rates: List) -> bytes:
        rates_len = len(rates)
        old_max = max(rates)
        old_min = min(rates)
        new_max = 255
        new_min = 0

        old_range = (old_max - old_min)
        new_range = (new_max - new_min)

        for max_n in range(rates_len):
            if max_n * max_n > rates_len: break

        img_array = np.full((max_n, max_n, 3), [0, 255, 0], dtype=np.uint8)

        x, y = 0, 0
        for n in rates:
            color = (255 - (((n - old_min) * new_range) / old_range) + new_min)
            img_array[x][y] = [color, color, color]
            if y < max_n-1: y += 1
            else:
                x += 1
                y = 0

        return DataOperations.__array_to_bytes_image(img_array)