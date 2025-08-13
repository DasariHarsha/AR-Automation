print_time=True

def print_and_log(msg, file_handle, color=None):
    if color == 'green':
        # Print in green in console, plain in log file
        print(f"\033[92m{msg}\033[0m")
        file_handle.write(msg + '\n')
    else:
        print(msg)
        file_handle.write(msg + '\n')

def print_summary(summary, app_summary, start_time, end_time, report_name):
    with open('Files/logs.txt', 'a', encoding='utf-8') as f:
        print_and_log(f"\n\nStart Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}  End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}  for {report_name}\n", f, color='green')
        print_time=False
        print_and_log("\n--- Overall Automation Summary for Assessment Questionaire---", f)
        print_and_log(f"Total applications processed: {len(summary['applications'])}", f)
        print_and_log(f"Total hostnames with R-Strategy updated: {len(summary['updated'])}", f)
        print_and_log(f"Total hostnames not updated: {len(summary['not_updated'])}", f)
        print_and_log(f"Hostnames not updated: {summary['not_updated']}", f)
        print_and_log(f"Total error hostnames: {len(summary['error_hostnames'])}", f)
        print_and_log(f"error hostnames: {summary['error_hostnames']}", f)
        print_and_log(f"Total Rehost: {len(summary['rehost'])}", f)
        print_and_log(f"Total Replatform: {len(summary['replatform'])}", f)
        print_and_log("\n--- Application-wise Summary ---", f)
        for app in summary['applications']:
            print_and_log(f"\nApplication: {app}", f)
            print_and_log(f"  Hostnames with R-Strategy updated: {len(app_summary[app]['updated'])}", f)
            print_and_log(f"  Hostnames not updated: {len(app_summary[app]['not_updated'])}", f)
            print_and_log(f"  Not updated hostnames: {app_summary[app]['not_updated']}", f)
            print_and_log(f"  No of Error hostnames: {len(app_summary[app]['error_hostnames'])}", f)
            print_and_log(f"  Error hostnames: {app_summary[app]['error_hostnames']}", f)
            print_and_log(f"  Rehost: {len(app_summary[app]['rehost'])}", f)
            print_and_log(f"  Replatform: {len(app_summary[app]['replatform'])}", f)


def print_summary_for_RecommendationSelection(summary, app_summary, start_time, end_time, report_name):
    with open('Files/logs.txt', 'a', encoding='utf-8') as f:
        if print_time:
            print_and_log(f"\n\nStart Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}  End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}  for {report_name}\n", f, color='green')
        print_and_log("\n--- Overall Automation Summary For Recommendation Selection ---", f)
        print_and_log(f"Total applications processed: {len(summary['applications'])}", f)
        print_and_log(f"Total hostnames with Instance updated: {len(summary['updated'])}", f)
        print_and_log(f"Total hostnames not updated while trying to update: {len(summary['not_updated'])}", f)
        print_and_log(f"Hostnames not updated: {summary['not_updated']}", f)
        print_and_log(f"Total error hostnames: {len(summary['error_hostnames'])}", f)
        print_and_log(f"Error hostnames: {summary['error_hostnames']}", f)
        print_and_log("\n--- Application-wise Summary ---", f)
        for app in summary['applications']:
            print_and_log(f"\nApplication: {app}", f)
            print_and_log(f"  Hostnames with Instance updated: {len(app_summary[app]['updated'])}", f)
            print_and_log(f"  Hostnames not updated while trying to update: {len(app_summary[app]['not_updated'])}", f)
            print_and_log(f"  Not updated hostnames: {app_summary[app]['not_updated']}", f)
            print_and_log(f"  No of Error hostnames: {len(app_summary[app]['error_hostnames'])}", f)
            print_and_log(f"  Error hostnames: {summary['error_hostnames']}", f)
        print_and_log("\n***********************************************************************************************************************************************************", f)
        print_and_log("\n***********************************************************************************************************************************************************", f)