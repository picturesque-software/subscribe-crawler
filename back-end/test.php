<?php
///testing
include 'info_register.php';

// $websites = array('website1', 'website2'); 
// $subtime = array(InfoRegister::RegisterType_1, InfoRegister::RegisterType_2);
// //InfoRegister::addSubscribe(2, '112', '12d', $websites, $sendTime);
// $websites[1]='wb';

// InfoRegister::addSubscribe('001', 'test1@qq.com','', $websites, $subtime);
// InfoRegister::updateSubscribe('001', 'test2@qq.com','', $websites, $subtime);
// InfoRegister::updateWebsite(1, 'www.test1.com', 'test1', InfoRegister::UpdateWebsiteModeAdd);
// InfoRegister::updateWebsite(2, 'www.test2.com', 'test2', InfoRegister::UpdateWebsiteModeAdd);
// InfoRegister::updateWebsite(2, 'www.test3.com', 'test3', InfoRegister::UpdateWebsiteModeAdd);
// InfoRegister::updateWebsite(1, 'www.test1.com', 'test1', InfoRegister::UpdateWebsiteModeDelete);
// InfoRegister::updateWebsiteData($arr1, InfoRegister::UpdateWebsiteModeAdd);
// InfoRegister::updateWebsiteData($arr2, InfoRegister::UpdateWebsiteModeAdd);
// InfoRegister::updateWebsiteData($arr1, InfoRegister::UpdateWebsiteModeDelete);
// InfoRegister::updateWebsiteData($arr2, InfoRegister::UpdateWebsiteModeDelete);

// $email_arr = array(
//     'Lihua' => '123456789@qq.com',
//     'ZhangSan' => '987654321@qq.com'
// );

// InfoRegister::sendEmail($email_arr)

//InfoRegister::Broadcast(InfoRegister::AllType);

//InfoRegister::clearTable(InfoRegister::websites_data_table);

$websites = array(12, 14);
$subtime = array(InfoRegister::AllType, InfoRegister::AllType);
//InfoRegister::addSubscribe(1, "123456789@qq.com", "", $websites, $subtime);
//InfoRegister::updateWebsite(12, "www.baidu.com", "百度", InfoRegister::UpdateWebsiteModeAdd);
//InfoRegister::updateWebsite(14, "github.com", "github", InfoRegister::UpdateWebsiteModeAdd);
//InfoRegister::updateWebsite(16, "nju.cdu.cn", "NJU", InfoRegister::UpdateWebsiteModeAdd);
$arr1 = array('_id'=>1, 
    'web_name'=>'1d2', 
    'news_source_code'=>'wqefq3r', 
    'news_author'=>'me', 
    'news_title'=>'hahaha', 
    'news_pub_time'=>'2021.8.22');

$arr2 = array('_id'=>2, 
    'web_name'=>'百度', 
    'news_source_code'=>'wqefq3rwg3   g4evf3q4gq34g3q4gqwv qwefwqefqwefwq wq4fe3q4fcwwqec 0000000000000000000000', 
    'news_author'=>'me', 
    'news_title'=>'hahaha', 
    'news_pub_time'=>'2021.8.22');
InfoRegister::Broadcast(InfoRegister::AllType);
InfoRegister::updateWebsiteData($arr1, InfoRegister::UpdateWebsiteModeAdd);
InfoRegister::updateWebsiteData($arr2, InfoRegister::UpdateWebsiteModeAdd);

///
?>