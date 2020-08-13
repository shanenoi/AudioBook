# this code to explane why determin MEM_EACH (by vietnamese)
printf 'nghiên %.0s' {1..10} > temp
python3 main.py temp::vi &

echo "" > meom
while [ 1 ];
do
	pid=$(ps a | grep "python3 main.py" | grep -Po "\d{3,9}");
	mem=$(pmap -x $pid | grep -Po " (\d+)$");
	code=$?
	echo $mem
	[ $code = 1 ] && rm temp && break;
done