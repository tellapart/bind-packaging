# Makefile for source rpm: bind
# $Id$
NAME := bind
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
