#!/bin/python

import os

import requests

commit_msg = str(os.environ['TRAVIS_COMMIT_MSG'])
tendrl_bug_id = None
tendrl_spec = None
github_base_url = "http://github.com"


# Extract "tendrl-bug-id" and "tendrl-spec" name from the commit message
for line in commit_msg.split("\n"):
    if "tendrl-bug-id" in line:
        try:
            tendrl_bug_id = line.split("tendrl-bug-id:")[-1].strip()
        except Exception as ex:
            print(ex)

    if "tendrl-spec" in line:
        try:
            tendrl_spec = line.split("tendrl-spec:")[-1].strip()
        except Exception as ex:
            print(ex)

if tendrl_bug_id is None:
    raise Exception("Please add 'tendrl-bug-id:<tendrl_repo>/issue_id' to "
                    "your commit msg")

if tendrl_bug_id:
    issue = "%s/%s" % (github_base_url, tendrl_bug_id.replace("#", "/issues/"))
    if requests.get(issue).status_code != 200:
        raise Exception("Tendrl Bug specified in git commit msg not "
                        "found!!\n"
                        "%s" % issue)
    print("Tendrl Bug specified in git commit msg found!!\n%s" % issue)

if tendrl_spec:
    spec = "%s/%s.adoc" % ("https://github.com/Tendrl/specifications/tree"
                           "/master/specs", tendrl_spec)
    if requests.get(spec).status_code != 200:
        raise Exception("Tendrl Spec specified in git commit msg not found\n"
                        "%s" % spec)
print("Tendrl Spec specified in git commit msg found!!\n%s" % spec)
