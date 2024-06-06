#!/bin/fish
set output (echo $HOME)/Downloads/集群架构说明-计算服务.docx
pandoc -s --reference-doc template-word.docx 集群架构说明.md -o $output
echo 已转换为Word文件到$output
