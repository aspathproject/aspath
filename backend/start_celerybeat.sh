#!/bin/bash

celery -A worker beat -S redisbeat.RedisScheduler -l INFO
