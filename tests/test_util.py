import pytest
import util as util

@pytest.mark.first
@pytest.mark.parametrize(
    "line_num, limit",
    [(5, 10), (7, 10), (0, None), (None, None), (0, 1)],
)
def test_first(line_num, limit):
    assert util.first(line_num, limit)


@pytest.mark.first
@pytest.mark.parametrize("line_num, limit", [(15, 10), (8, 8), (0, 0), (17, 10), (9, 8), (1, 0)])
def test_first_negative(line_num, limit):
    assert not util.first(line_num, limit)


@pytest.mark.last
@pytest.mark.parametrize(
    "line_num, limit, line_count",
    [
        (15, 10, 15),
        (17, 10, 18),
        (19, 18, 20),
        (200, 200, 200),
        (1, 1, 1),
        (0, None, 1),
        (None, None, None),
        (1, 2, 3),
        (0, 0, 0)
    ],
)
def test_last(line_num, limit, line_count):
    assert util.last(line_num, limit, line_count)


@pytest.mark.last
@pytest.mark.parametrize(
    "line_num, limit, line_count",
    [(5, 10, 20), (7, 10, 200), (0, 1, 3), (0, 1, 2), (0, 0, 1)],
)
def test_last_negative(line_num, limit, line_count):
    assert not util.last(line_num, limit, line_count)


format = r"([01][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])"


@pytest.mark.check_time
@pytest.mark.parametrize(
    "line, format",
    [
        (
            "Jul 27 14:41:59 combo hcid[1690]: HCI daemon ver 2.4 started",
            format,
        ),
        (
            "Jul 26 05:47:42 combo ftpd[28686]: connection from 172.181.208.156 () at Tue Jul 26 05:47:42 2005 ",
            format,
        ),
        (
            "Jul 26 07:02:27 combo sshd(pam_unix)[28842]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=207.243.167.114  user=root",
            format,
        ),
        (
            "Jul 25 04:03:58 combo su(pam_unix)[24312]: session opened for user cyrus by (uid=0)",
            format,
        ),
        (
            "Jul 17 23:21:54 combo ftpd[25232]: connection from 82.68.222.195 (82-68-222-195.dsl.in-addr.zen.co.uk) at Sun Jul 17 23:21:54 2005 ",
            format,
        ),
        (
            "Jul 17 04:08:23 combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 04:08:23 combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 Rohan04:08:23 combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 04:08:23Rohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 Rohan combo logrotate: ALERT exited abnormally with [1]04:08:23",
            format,
        ),
        (
            "Rohan test Jul 17 Rohan04:08:23 combo logrotate: ALERT exited abnormally with [1] 99:99:99",
            format,
        ),
        (
            "Rohan test Jul 17 Rohan04:08:23Rohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 Rohan00:00:00Rohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 Rohan23:59:59Rohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            r"Rohan test Jul 17 Rohan\04:08:23\Rohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "04:08:23",
            format,
        ),
        (
            r"Rohan test Jul 17 Rohan04:08:23\Rohan combo logrotate: ALERT exited abnormally with [1]",
            None,
        ),
        (
            r"Rohan test Jul 17 Rohan\Rohan combo logrotate: ALERT exited abnormally with [1]",
            None,
        ),
    ],
)
def test_check_time(line, format):
    assert util.check_time(line, format)


@pytest.mark.check_time
@pytest.mark.parametrize(
    "line, format",
    [
        (
            "Rohan test Jul 17 Rohan99:99:99Rohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 Rohan24:00:00Rohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 Rohan00:60:00Rohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 Rohan00:00:60Rohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
        (
            "Rohan test Jul 17 RohanRohan combo logrotate: ALERT exited abnormally with [1]",
            format,
        ),
    ],
)
def test_check_time_negative(line, format):
    assert not util.check_time(line, format)


ip_test_data = [
    # Valid IPv4 address, exact match
    ("This is an IP: 192.168.1.1", "192.168.1.1", "ipv4", (True, "This is an IP: \033[44m192.168.1.1\033[0m")),
    # Valid IPv4 address, no match
    ("This is an IP: 192.168.1.2", "192.168.1.1", "ipv4", (False, "This is an IP: 192.168.1.2")),
    # Valid IPv6 address, exact match
    ("IPv6 address: 2001:db8::1", "2001:db8::1", "ipv6", (True, "IPv6 address: \033[44m2001:db8::1\033[0m")),
    # Valid IPv6 address, no match
    ("IPv6 address: 2001:db8::2", "2001:db8::1", "ipv6", (False, "IPv6 address: 2001:db8::2")),
    # Boolean matching for any IPv4 address
    ("Multiple IPs: 192.168.1.1 and 10.0.0.1", True, "ipv4", (True, "Multiple IPs: \033[44m192.168.1.1\033[0m and \033[44m10.0.0.1\033[0m")),
    # Boolean matching for any IPv6 address
    ("IPv6 list: 2001:db8::1 2001:db8::2", True, "ipv6", (True, "IPv6 list: \033[44m2001:db8::1\033[0m \033[44m2001:db8::2\033[0m")),
    # Invalid IP address in text
    ("Invalid IP: 999.999.999.999", "192.168.1.1", "ipv4", (False, "Invalid IP: 999.999.999.999")),
    # Mixed valid and invalid IPs
    ("Mixed IPs: 192.168.1.1 999.999.999.999", True, "ipv4", (True, "Mixed IPs: \033[44m192.168.1.1\033[0m 999.999.999.999")),
    # Empty string
    ("", "192.168.1.1", "ipv4", (False, "")),
    # None as IP address
    ("This is an IP: 192.168.1.1", None, "ipv4", (True, "This is an IP: 192.168.1.1")),
    # Edge case: text with no IPs
    ("No IPs here", "192.168.1.1", "ipv4", (False, "No IPs here")),
    # Edge case: Boolean matching for empty text
    ("", True, "ipv4", (False, "")),
]

@pytest.mark.parametrize("text, ip_address, ip_type, expected", ip_test_data)
def test_highlight_ip(text, ip_address, ip_type, expected):
    assert util.highlight_ip(text, ip_address, ip_type) == expected