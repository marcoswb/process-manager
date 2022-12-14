#!/bin/bash

pid_array=`ls /proc | grep -E '^[0-9]+$'`
clock_ticks=$(getconf CLK_TCK)
total_memory=$( grep -Po '(?<=MemTotal:\s{8})(\d+)' /proc/meminfo )

cat /dev/null > .data.ps

for pid in $pid_array
do
    if [ -r /proc/$pid/stat ]
    then
        stat_array=( `sed -E 's/(\([^\s)]+)\s([^)]+\))/\1_\2/g' /proc/$pid/stat` )
        uptime_array=( `cat /proc/uptime` )
        statm_array=( `cat /proc/$pid/statm` )
        comm=( `grep -Po '^[^\s\/]+' /proc/$pid/comm` )
        user_id=$( grep -Po '(?<=Uid:\s)(\d+)' /proc/$pid/status )

        user=$( id -nu $user_id )
        uptime=${uptime_array[0]}

        state=${stat_array[2]}
        ppid=${stat_array[3]}
        priority=${stat_array[17]}
        nice=${stat_array[18]}

        utime=${stat_array[13]}
        stime=${stat_array[14]}
        cutime=${stat_array[15]}
        cstime=${stat_array[16]}
        num_threads=${stat_array[19]}
        starttime=${stat_array[21]}

        total_time=$(( $utime + $stime ))
        #add $cstime - CPU time spent in user and kernel code ( can olso add $cutime - CPU time spent in user code )
        total_time=$(( $total_time + $cstime ))
        seconds=$( awk 'BEGIN {print ( '$uptime' - ('$starttime' / '$clock_ticks') )}' )
        cpu_usage=$( awk 'BEGIN {print ( 100 * (('$total_time' / '$clock_ticks') / '$seconds') )}' )

        resident=${statm_array[1]}
        data_and_stack=${statm_array[5]}
        memory_usage=$( awk 'BEGIN {print( (('$resident' + '$data_and_stack' ) * 100) / '$total_memory'  )}' )

        printf "%-6d %-6d %-10s %-4d %-5d %-4s %-4u %-7.2f %-7.2f %-18s\n" $pid $ppid $user $priority $nice $state $num_threads $memory_usage $cpu_usage $comm >> .data.ps

    fi
done

clear
printf "\e[30;107m%-6s %-6s %-10s %-4s %-3s %-6s %-4s %-7s %-7s %-18s\e[0m\n" "PID" "PPID" "USER" "PR" "NI" "STATE" "THR" "%MEM" "%CPU" "COMMAND"
sort -nr -k9 .data.ps | head -$1
read_options
    