__author__ = 'Dave'



def retrieve_dashboard_posts_by_month(start, end):
    month_metrics = []

    temp_metric = dashboard_posts_metric()
    temp_metric.month = "Jan 2014"
    temp_metric.num_posts = 98

    month_metrics.append(temp_metric)

    temp_metric = dashboard_posts_metric()
    temp_metric.month = "Feb 2014"
    temp_metric.num_posts = 89

    month_metrics.append(temp_metric)

    temp_metric = dashboard_posts_metric()
    temp_metric.month = "Mar 2014"
    temp_metric.num_posts = 77

    month_metrics.append(temp_metric)

    temp_metric = dashboard_posts_metric()
    temp_metric.month = " Apr 2014"
    temp_metric.num_posts = 76

    month_metrics.append(temp_metric)

    temp_metric = dashboard_posts_metric()
    temp_metric.month = "May 2014"
    temp_metric.num_posts = 54

    month_metrics.append(temp_metric)

    return month_metrics

class dashboard_posts_metric():
    month =  None
    num_posts = 0
