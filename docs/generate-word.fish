#!/bin/fish
set output (echo $HOME)/Downloads/
pandoc -s --reference-doc template-word.docx 集群架构说明.md -o $output/集群架构说明-计算服务.docx
pandoc -s --reference-doc template-word.docx 后端环境变量配置.md -o $output/环境变量配置.docx
echo 已转换为Word文件到$output
