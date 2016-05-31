from jenkins_ycny import AboutJenkinsDialog


def test_AboutJenkinsDialog_members():
    expected_members = [
        'AboutDialog', 'AboutJenkinsDialog', 'logger', 'logging'
    ]

    all_members = dir(AboutJenkinsDialog)

    public_members = [x for x in all_members if not x.startswith('_')]
    public_members.sort()

    assert expected_members == public_members
