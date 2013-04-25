#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import fileinput
import email
from email.header import decode_header
from email.Iterators import typed_subpart_iterator
from email.parser import FeedParser

def get_header(header_text, default="ascii"):
    headers = decode_header(header_text)
    header_parts = [unicode(text, charset or default) for text, charset in headers]
    return u"".join(header_parts)

def get_charset(message, default="ascii"):
    if message.get_content_charset():
        return message.get_content_charset()
    if message.get_charset():
        return message.get_charset()
    return default

def get_body(message):
    if message.is_multipart():
        # payload is an iterator of sub-parts
        text_parts = [part for part in typed_subpart_iterator(message, 'text', 'plain')]
        body = []
        for part in text_parts:
            charset = get_charset(part, get_charset(message))
            body.append(unicode(part.get_payload(decode=True), encoding=charset, errors="replace"))

        return u"\n".join(body).strip()

    else: 
        # payload is a string
        body = unicode(message.get_payload(decode=True), encoding=get_charset(message), errors="replace")
        return body.strip()

def read_msg():
    parser = FeedParser()
    for line in fileinput.input():
        parser.feed(line)
    return parser.close()

msg = read_msg()

if not msg:
    sys.stderr.write("Sorry, failed to parse email\n")
    sys.exit(1)

for header_key in msg.keys():
    header_value = get_header(msg[header_key])
    print "%s: %s" % (header_key, header_value)

print get_body(msg)
