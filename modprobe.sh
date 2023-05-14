#!/bin/sh

password="bioskop"

# Use the password to answer the sudo command
echo "$password" | sudo -S modprobe v4l2loopback

