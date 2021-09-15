import pyecharts.options as opts
from pyecharts.charts import WordCloud

data = []

def initData(words, counts):
    for i in range(len(words)):
        data.append((words[i], counts[i]))


def wordCloud(words, counts) -> WordCloud:
    initData(words,counts)
    c = (
    WordCloud()
    .add(series_name="敏感词统计", data_pair=data, shape="circle", word_size_range=[6, 66])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="敏感词统计", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
    .render("sensitiveWordCloud.html")
    )
    return c