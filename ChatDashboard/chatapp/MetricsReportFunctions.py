__author__ = 'Dave'



def retrieve_dashboard_posts_by_month(start, end):
    month_metrics = []

    temp_metric = dashboard_posts_metric()
    temp_metric.month = "01/2014"
    temp_metric.num_posts = 20

    month_metrics.append(temp_metric)

    temp_metric = dashboard_posts_metric()
    temp_metric.month = "02/2014"
    temp_metric.num_posts = 35

    month_metrics.append(temp_metric)

    return month_metrics

class dashboard_posts_metric():
    month =  None
    num_posts = 0
