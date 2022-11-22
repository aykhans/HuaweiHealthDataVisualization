import pandas as pd
from datetime import (datetime,
                    timedelta)
from typing import (List,
                    Tuple,
                    Union)


class DataOperations:
    heart_rate = None

    def is_data_none_wrapper(func):
        def __is_data_none(self, *args, **kwargs) -> Union[None, NameError]:
            if self.data is None:
                raise NameError(f'data not found. You must call the get_data function before calling the {func.__name__} function')
            return func(self, *args, **kwargs)
        return __is_data_none

    def is_heart_rate_none_wrapper(func):
        def __is_heart_rate_none(self, *args, **kwargs) -> Union[None, NameError]:
            if self.heart_rate is None:
                raise NameError(f'heart_rate data not found. You must call the get_heart_rate function before calling the {func.__name__} function')
            return func(self, *args, **kwargs)
        return __is_heart_rate_none

    @is_data_none_wrapper
    def get_heart_rate(self) -> List:
        # sourcery skip: inline-immediately-returned-variable, list-comprehension
        self.heart_rate = []
        for d in self.data:
            if d['type'] == 7:
                self.heart_rate.append(
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
        return self.heart_rate

    @is_heart_rate_none_wrapper
    def get_heart_rate_for_all_days_as_axis(self) -> Tuple:
        heart_rate = pd.DataFrame(self.heart_rate)
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
                    lambda t: {'rate': t['rate'], 'date': t['time'].strftime("%d-%m-%Y")}, self.heart_rate
                )
            )
        ).groupby('date', sort=False).mean()['rate']

        return (heart_rate_grouped.keys(), heart_rate_grouped.values)

    @is_heart_rate_none_wrapper
    def get_heart_rate_for_one_day(self, day) -> Tuple:
        heart_rate = pd.DataFrame(
            list(
                filter(
                    lambda t: t['time'].strftime("%d-%m-%Y") == day, self.heart_rate
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