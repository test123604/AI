#---test1-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=read -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest1 >> /home/auto_capture_log/log_data/fiotest1.log
sleep 1
#---test2-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=read -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest2 >> /home/auto_capture_log/log_data/fiotest2.log
sleep 1
#---test3-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=read -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest3 >> /home/auto_capture_log/log_data/fiotest3.log
sleep 1
#---test4-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=read -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest4 >> /home/auto_capture_log/log_data/fiotest4.log
sleep 1
#---test5-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=read -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest5 >> /home/auto_capture_log/log_data/fiotest5.log
sleep 1
#---test6-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=read -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest6 >> /home/auto_capture_log/log_data/fiotest6.log
sleep 1
#---test7-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=read -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest7 >> /home/auto_capture_log/log_data/fiotest7.log
sleep 1
#---test8-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=read -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest8 >> /home/auto_capture_log/log_data/fiotest8.log
sleep 1
#---test9-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=read -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest9 >> /home/auto_capture_log/log_data/fiotest9.log
sleep 1
#---test10-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=read -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest10 >> /home/auto_capture_log/log_data/fiotest10.log
sleep 1
#---test11-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=read -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest11 >> /home/auto_capture_log/log_data/fiotest11.log
sleep 1
#---test12-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=read -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest12 >> /home/auto_capture_log/log_data/fiotest12.log
sleep 1
#---test13-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=read -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest13 >> /home/auto_capture_log/log_data/fiotest13.log
sleep 1
#---test14-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=read -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest14 >> /home/auto_capture_log/log_data/fiotest14.log
sleep 1
#---test15-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=write -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest15 >> /home/auto_capture_log/log_data/fiotest15.log
sleep 1
#---test16-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=write -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest16 >> /home/auto_capture_log/log_data/fiotest16.log
sleep 1
#---test17-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=write -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest17 >> /home/auto_capture_log/log_data/fiotest17.log
sleep 1
#---test18-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=write -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest18 >> /home/auto_capture_log/log_data/fiotest18.log
sleep 1
#---test19-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=write -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest19 >> /home/auto_capture_log/log_data/fiotest19.log
sleep 1
#---test20-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=write -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest20 >> /home/auto_capture_log/log_data/fiotest20.log
sleep 1
#---test21-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=write -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest21 >> /home/auto_capture_log/log_data/fiotest21.log
sleep 1
#---test22-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=write -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest22 >> /home/auto_capture_log/log_data/fiotest22.log
sleep 1
#---test23-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=write -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest23 >> /home/auto_capture_log/log_data/fiotest23.log
sleep 1
#---test24-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=write -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest24 >> /home/auto_capture_log/log_data/fiotest24.log
sleep 1
#---test25-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=write -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest25 >> /home/auto_capture_log/log_data/fiotest25.log
sleep 1
#---test26-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=write -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest26 >> /home/auto_capture_log/log_data/fiotest26.log
sleep 1
#---test27-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=write -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest27 >> /home/auto_capture_log/log_data/fiotest27.log
sleep 1
#---test28-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=write -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest28 >> /home/auto_capture_log/log_data/fiotest28.log
sleep 1
#---test29-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randread -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest29 >> /home/auto_capture_log/log_data/fiotest29.log
sleep 1
#---test30-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randread -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest30 >> /home/auto_capture_log/log_data/fiotest30.log
sleep 1
#---test31-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randread -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest31 >> /home/auto_capture_log/log_data/fiotest31.log
sleep 1
#---test32-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randread -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest32 >> /home/auto_capture_log/log_data/fiotest32.log
sleep 1
#---test33-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randread -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest33 >> /home/auto_capture_log/log_data/fiotest33.log
sleep 1
#---test34-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randread -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest34 >> /home/auto_capture_log/log_data/fiotest34.log
sleep 1
#---test35-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randread -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest35 >> /home/auto_capture_log/log_data/fiotest35.log
sleep 1
#---test36-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randread -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest36 >> /home/auto_capture_log/log_data/fiotest36.log
sleep 1
#---test37-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randread -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest37 >> /home/auto_capture_log/log_data/fiotest37.log
sleep 1
#---test38-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randread -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest38 >> /home/auto_capture_log/log_data/fiotest38.log
sleep 1
#---test39-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randread -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest39 >> /home/auto_capture_log/log_data/fiotest39.log
sleep 1
#---test40-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randread -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest40 >> /home/auto_capture_log/log_data/fiotest40.log
sleep 1
#---test41-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randread -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest41 >> /home/auto_capture_log/log_data/fiotest41.log
sleep 1
#---test42-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randread -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest42 >> /home/auto_capture_log/log_data/fiotest42.log
sleep 1
#---test43-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randwrite -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest43 >> /home/auto_capture_log/log_data/fiotest43.log
sleep 1
#---test44-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randwrite -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest44 >> /home/auto_capture_log/log_data/fiotest44.log
sleep 1
#---test45-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randwrite -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest45 >> /home/auto_capture_log/log_data/fiotest45.log
sleep 1
#---test46-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randwrite -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest46 >> /home/auto_capture_log/log_data/fiotest46.log
sleep 1
#---test47-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randwrite -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest47 >> /home/auto_capture_log/log_data/fiotest47.log
sleep 1
#---test48-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randwrite -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest48 >> /home/auto_capture_log/log_data/fiotest48.log
sleep 1
#---test49-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randwrite -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest49 >> /home/auto_capture_log/log_data/fiotest49.log
sleep 1
#---test50-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randwrite -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest50 >> /home/auto_capture_log/log_data/fiotest50.log
sleep 1
#---test51-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randwrite -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest51 >> /home/auto_capture_log/log_data/fiotest51.log
sleep 1
#---test52-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randwrite -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest52 >> /home/auto_capture_log/log_data/fiotest52.log
sleep 1
#---test53-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randwrite -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest53 >> /home/auto_capture_log/log_data/fiotest53.log
sleep 1
#---test54-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randwrite -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest54 >> /home/auto_capture_log/log_data/fiotest54.log
sleep 1
#---test55-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randwrite -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest55 >> /home/auto_capture_log/log_data/fiotest55.log
sleep 1
#---test56-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randwrite -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest56 >> /home/auto_capture_log/log_data/fiotest56.log
sleep 1
#---test57-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest57 >> /home/auto_capture_log/log_data/fiotest57.log
sleep 1
#---test58-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest58 >> /home/auto_capture_log/log_data/fiotest58.log
sleep 1
#---test59-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest59 >> /home/auto_capture_log/log_data/fiotest59.log
sleep 1
#---test60-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest60 >> /home/auto_capture_log/log_data/fiotest60.log
sleep 1
#---test61-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest61 >> /home/auto_capture_log/log_data/fiotest61.log
sleep 1
#---test62-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest62 >> /home/auto_capture_log/log_data/fiotest62.log
sleep 1
#---test63-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=4k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest63 >> /home/auto_capture_log/log_data/fiotest63.log
sleep 1
#---test64-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=1 -iodepth=1 -name=fiotest64 >> /home/auto_capture_log/log_data/fiotest64.log
sleep 1
#---test65-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=4 -iodepth=1 -name=fiotest65 >> /home/auto_capture_log/log_data/fiotest65.log
sleep 1
#---test66-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=8 -iodepth=1 -name=fiotest66 >> /home/auto_capture_log/log_data/fiotest66.log
sleep 1
#---test67-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=16 -iodepth=1 -name=fiotest67 >> /home/auto_capture_log/log_data/fiotest67.log
sleep 1
#---test68-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=32 -iodepth=1 -name=fiotest68 >> /home/auto_capture_log/log_data/fiotest68.log
sleep 1
#---test69-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=64 -iodepth=1 -name=fiotest69 >> /home/auto_capture_log/log_data/fiotest69.log
sleep 1
#---test70-------------------------------
date +"%Y-%m-%d %H-%M-%S"
echo y | mkfs.ext4 /dev/sdc
mount -t ext4 -o discard /dev/sdc /mnt/
fstrim -v /mnt/
umount /mnt/
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 1
free -h
echo fio running...
fio -filename=/dev/sdc -thread -runtime=300 -group_reporting -bs=64k -direct=1 -rw=randrw -rwmixread=70 -ioengine=psync -numjobs=128 -iodepth=1 -name=fiotest70 >> /home/auto_capture_log/log_data/fiotest70.log
sleep 1
