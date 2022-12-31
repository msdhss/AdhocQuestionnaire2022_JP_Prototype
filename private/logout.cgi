#!/usr/bin/perl
print <<EOF;
HTTP/1.0 401 Unauthorized
WWW-Authenticate: Basic Realm="valid users only"
Content-Type: text/html

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML><HEAD><TITLE>401 Authorization Required</TITLE></HEAD>
<BODY>
<H1>Authorization Required</H1>
</BODY>
</HTML>
EOF
