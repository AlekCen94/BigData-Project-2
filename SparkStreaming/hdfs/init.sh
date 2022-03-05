#!/bin/bash

sh bootstrap.sh -bash
hadoop dfsadmin -safemode wait
hadoop dfs -mkdir /data
hadoop dfs -put /opt/hadoopspark/ /data



