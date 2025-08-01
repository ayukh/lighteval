# MIT License

# Copyright (c) 2024 The HuggingFace Team

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dataclasses import dataclass
from typing import Callable

from lighteval.tasks.requests import SamplingMethod


@dataclass
class Metric:
    metric_name: str
    higher_is_better: bool
    category: SamplingMethod
    sample_level_fn: Callable
    corpus_level_fn: Callable

    batched_compute: bool = False

    def get_doc(self):
        return self.sample_level_fn.__doc__

    def compute(
        self, **kwargs
    ) -> dict:  # result: Union[list[ModelResponse], ModelResponse], formatted_doc: Doc) -> dict:
        if isinstance(self, MetricGrouping):
            return self.sample_level_fn(**kwargs)  # result, formatted_doc,
        return {self.metric_name: self.sample_level_fn(**kwargs)}  # result, formatted_doc,


@dataclass
class MetricGrouping(Metric):
    """Some metrics are more advantageous to compute together at once.
    For example, if a costly preprocessing is the same for all metrics, it makes more sense to compute it once.
    """

    metric_name: list[str]
    corpus_level_fn: dict[str, Callable]
    higher_is_better: dict[str, Callable]


@dataclass
class CorpusLevelMetric(Metric):
    """Metric computed over the whole corpora, with computations happening at the aggregation phase"""

    pass


@dataclass
class SampleLevelMetric(Metric):
    """Metric computed per sample, then aggregated over the corpus"""

    pass


@dataclass
class CorpusLevelMetricGrouping(MetricGrouping):
    """MetricGrouping computed over the whole corpora, with computations happening at the aggregation phase"""

    pass


@dataclass
class SampleLevelMetricGrouping(MetricGrouping):
    """MetricGrouping are computed per sample, then aggregated over the corpus"""

    pass
