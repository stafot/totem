import click
import json
import sys

from temcheck.checks.suite import CheckSuite
from temcheck.github.content import ContentProviderFactory
from temcheck.github.utils import parse_pr_url

@click.command()
@click.option('-p', '--pr-url', required=True, type=str)
@click.option('-c', '--config-file', required=True, type=str)
def main(pr_url, config_file):
    full_repo_name, pr_number = parse_pr_url(pr_url)
    factory = ContentProviderFactory(full_repo_name, pr_number)
    f = open(config_file, 'r')
    config = json.load(f)

    suite = CheckSuite(config, factory)
    suite.run()

    failed_check = None
    for result in suite.results.results.items():
        if not result[1].success:
            failed_check = True
            print(result[1].details)
    if failed_check is not None:
        sys.exit(1)
