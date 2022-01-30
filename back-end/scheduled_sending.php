<?php
include 'info_register.php';

date_default_timezone_set('Asia/Shanghai');

$cur_time = strtotime(date('H:i'));
$morning_time = strtotime(date('08:00'));
$lunch_time = strtotime(date('12:00'));
$dinner_time = strtotime(date('18:00'));
$night_time = strtotime(date('22:00'));

$ten_minutes = 600;
$mode = 1;
if($cur_time >= $morning_time - $ten_minutes && $cur_time <= $morning_time + $ten_minutes)
{
    $mode <<= 0;
}
else if($cur_time >= $lunch_time - $ten_minutes && $cur_time <= $lunch_time + $ten_minutes)
{
    $mode <<= 1;
}
else if($cur_time >= $dinner_time - $ten_minutes && $cur_time <= $dinner_time + $ten_minutes)
{
    $mode <<= 2;
}
else if($cur_time >= $night_time - $ten_minutes && $cur_time <= $night_time + $ten_minutes)
{
    $mode <<= 3;
}
else 
{
    $mode = 0;
}

InfoRegister::Broadcast($mode);
?>