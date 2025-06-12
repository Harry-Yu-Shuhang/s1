#!/bin/bash
set -e

# 文件名：s1.sif
DEF=apptainer.def
SIF=s1.sif

if [ -f "$SIF" ]; then
  echo "✅ 已存在 $SIF，跳过构建。如需重新构建请先删除。"
else
  echo "🚧 构建 $SIF..."
  apptainer build --fakeroot $SIF $DEF
fi
