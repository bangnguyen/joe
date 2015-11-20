for KILLPID in `ps ax | grep scrapy | awk ' { print $1;}'`; do
echo $KILLPID
kill -9 $KILLPID || {
  echo "not found "  $KILLPID;
}
done
cd /root/joe
python run_all.py
