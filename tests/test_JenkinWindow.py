from jenkins_ycny.JenkinsWindow import extract_pair_users


def test_extract_pair_user():
    assert ['a'] == extract_pair_users('pair+a')
    assert ['a'] == extract_pair_users('a')
    assert 'a' in extract_pair_users('pair+a+b')
    assert 'b' in extract_pair_users('pair+a+b')
    assert 'c' not in extract_pair_users('pair+a+b')
