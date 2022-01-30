<?php
require 'config.php';

class InfoRegister{
    public const RegisterType_Morning = 1;
    public const RegisterType_Lunch = 1 << 1; 
    public const RegisterType_Dinner = 1 << 2; 
    public const RegisterType_Night = 1 << 3; 
    public const RegisterType_5 = 1 << 4; 
    public const RegisterType_6 = 1 << 5; 
    public const AllType =  1 | 1<<1 | 1<<2 | 1<<3 | 1<<4 | 1<<5;
    public const UpdateWebsiteModeDelete = 1001;
    public const UpdateWebsiteModeAdd = 1002;
    public const user_register_table = "user_register_table";
    public const websites_table = "websites_table";
    public const websites_data_table = "websites_data_table";

    /**
     * 本函数负责用户订阅设置的装载
     * 邮箱验证应当在在本函数调用前完成
     * 对于已经注册过的用户本函数不作处理
     * @return bool 返回注册是否成功
     */
    public static function addSubscribe($uid, string $email, string $token, array $websites, array $subTime)
    {
        //检查token合法性
        if(!InfoRegister::checkToken($email, $token))
            return false;
        //检查$uid是否已经注册过
        if(InfoRegister::ifAreadyAdd($uid, InfoRegister::user_register_table))
        {
            //已经注册：不再处理
            return false;
        }

        //构造用户注册表并写入数据库
        $register_table = array('uid'=>$uid, 'u_mail'=>$email, 'website'=>$websites, 'subtime'=>$subTime);
        $register_status = InfoRegister::writeToDB($register_table);
        
        return $register_status;
    }

    /**
     * 更新订阅信息
     * @return bool 返回更新是否成功
     */
    public static function updateSubscribe($uid, string $email, string $token, array $websites, array $subTime)
    {
        //检查token合法性
        if(!InfoRegister::checkToken($email, $token))
        {   
            return false;
        }

        $register_table = array('uid'=>$uid, 'u_mail'=>$email, 'website'=>$websites, 'subtime'=>$subTime);
        $register_status = InfoRegister::updateToDB($register_table);
        
        return $register_status;
    }

    /**
     * 向网页表中添加网页
     * @return bool 返回添加状态
     */
    public static function updateWebsite($id, string $url, string $name, int $mode)
    {
        return InfoRegister::updateWebsiteTable($id, $url, $name, $mode);
    }

    //更新网页数据表
    public static function updateWebsiteData(array $data, int $mode)
    {
        $_id = $data['_id'];
        $web_name = $data['web_name'];
        $news_source_code = $data['news_source_code'];
        $news_author = $data['news_author'];
        $news_title = $data['news_title'];
        $news_pub_time = $data['news_pub_time'];
        if(!(isset($_id)&&isset($web_name)&& isset($news_source_code)&& isset($news_author)&&isset($news_title)&&isset($news_pub_time)))
        {
            return false;
        }

        $db = new mysqli(CONFIG::$db['host'], CONFIG::$db['user'], CONFIG::$db['pwd'], CONFIG::$db['dbname']);
        if($db->connect_error)
            return false;

        $sql = '';
        if($mode == InfoRegister::UpdateWebsiteModeAdd)
        {
            if(InfoRegister::ifAreadyAdd($_id, InfoRegister::websites_data_table))
            {
                $sql = 'UPDATE '.InfoRegister::websites_data_table.' SET 
                web_name=\''.$web_name.'\',
                news_source_code=\''.$news_source_code.'\',
                news_author=\''.$news_author.'\',
                news_title=\''.$news_title.'\',
                news_pub_time=\''.$news_pub_time.'\' 
                WHERE _id='.$_id;
            }
            else
            {
                $sql = 'INSERT INTO '.InfoRegister::websites_data_table.' (_id, web_name, news_source_code, news_author, news_title, news_pub_time) 
                VALUES('.$_id.', \''.$web_name.'\', \''.$news_source_code.'\', \''.$news_author.'\', \''.$news_title.'\', \''.$news_pub_time.'\')';
            }
        }
        else if($mode == InfoRegister::UpdateWebsiteModeDelete)
        {
            $sql = 'DELETE FROM '.InfoRegister::websites_data_table.' WHERE _id='.$_id;
        }

        $db->query($sql);
        $db->close();
        return true;
    }

    # with open('to_addrs.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for row in data:
#         writer.writerow(row)

    //array格式: arr('name'=>'addr')
    public static function sendEmail(array $info, array $text)
    {
        $fp = fopen("addrs.csv", "w");
        $index = 0;
        foreach($info as $name => $addr)
        {
            fwrite($fp,$name.",".$addr.",".$text[$index].",".$auth."\n");
            $index++;
        }
        fclose($fp);
        exec('python mail.py');
    }


    public static function Broadcast(int $mode)
    {
        $db = new mysqli(CONFIG::$db['host'], CONFIG::$db['user'], CONFIG::$db['pwd'], CONFIG::$db['dbname']);
        if($db->connect_error)
            return false;

        while($row = mysqli_fetch_row($result))
        {   
            $websites = explode(",", $row[2]);
            $modes = explode(",", $row[3]);
            $arr_size = count($websites);
            for($i=0; $i<$arr_size; $i++)
            {
                //满足推送条件
                if($modes[$i] & $mode != 0)
                {
                    $sql = "SELECT * FROM ".InfoRegister::websites_data_table." WHERE _id=".$websites[$i];
                    $result = $db->query($sql);
                    
                    //TODO: 处理网页数据并发送邮件

                }
            }
        }
        $db->close();
    }
    //表中是否有ID包含的项
    private static function ifAreadyAdd($uid, $table_name)
    {
        $db = new mysqli(CONFIG::$db['host'], CONFIG::$db['user'], CONFIG::$db['pwd'], CONFIG::$db['dbname']);
        if($db->connect_error)
            return false;

        $db->select_db('nxb');
        $sql = '';
        switch($table_name)
        {
            case InfoRegister::user_register_table: $sql = 'SELECT uid from '.$table_name.' where uid='.$uid; break;
            case InfoRegister::websites_table: $sql = 'SELECT web_id from '.$table_name.' where web_id='.$uid; break;
            case InfoRegister::websites_data_table: $sql = 'SELECT _id from '.$table_name.' where _id='.$uid; break;
            default: $db->close(); return false;
        }

        $res = mysqli_fetch_array($db->query($sql));
        $db->close();
        return $res != null;
    }

    //将数据表写入数据库
    private static function writeToDB(array $register_table)
    {
        $uid = $register_table['uid'];
        $mail = $register_table['u_mail'];
        $website = $register_table['website'];
        $subtime = $register_table['subtime'];


        $db = new mysqli(CONFIG::$db['host'], CONFIG::$db['user'], CONFIG::$db['pwd'], CONFIG::$db['dbname']);
        if($db->connect_error)
            return false;

        $sql = "INSERT INTO ".InfoRegister::user_register_table." (uid, u_mail, website, subtime)
                VALUES ('".$uid."', '".$mail."', '".implode(',',$website)."', '".implode(',',$subtime)."')";
        $db->query($sql);
        $db->close();
        return true;
    }

    //更新配置信息,要求表中已有对应项
    private static function updateToDB(array $register_table)
    {   
        $uid = $register_table['uid'];
        $mail = $register_table['u_mail'];
        $website = $register_table['website'];
        $subtime = $register_table['subtime'];

        if(!InfoRegister::ifAreadyAdd($uid, InfoRegister::user_register_table))  
        {
            return false;
        }


        $db = new mysqli(CONFIG::$db['host'], CONFIG::$db['user'], CONFIG::$db['pwd'], CONFIG::$db['dbname']);
        if($db->connect_error)
            return false;

        $sql = "UPDATE ".InfoRegister::user_register_table." SET ".
            "u_mail='".$mail."',".
            "website='".implode(',',$website)."',".
            "subtime='".implode(',',$subtime)."' where uid='".$uid."'";
        
        $db->query($sql);
        $db->close();
        return true;
    }


    private static function updateWebsiteTable($id, $url, string $name, $mode)
    {
        $db = new mysqli(CONFIG::$db['host'], CONFIG::$db['user'], CONFIG::$db['pwd'], CONFIG::$db['dbname']);
        if($db->connect_error)
            return false;
        $sql = '';
        switch($mode)
        {
            case InfoRegister::UpdateWebsiteModeAdd: 
                if(InfoRegister::ifAreadyAdd($id, InfoRegister::websites_table))
                {
                    $sql = 'UPDATE '.InfoRegister::websites_table.' SET web_url=\''.$url.'\', web_name=\''.$name.'\' 
                    WHERE web_id='.$id;
                }
                else
                {
                    $sql = 'INSERT INTO '.InfoRegister::websites_table.' (web_id, web_url, web_name) 
                    VALUES('.$id.', \''.$url.'\', \''.$name.'\')';
                }
                break;
            case InfoRegister::UpdateWebsiteModeDelete: 
                $sql = 'DELETE FROM '.InfoRegister::websites_table.' WHERE web_id='.$id;
                break;
            default: $db->close(); return false;
        }
        $db->query($sql);
        $db->close();
        return true;
    }

    //
    private static function checkToken($email, $token)
    {
        //现测试期间统统return true
        return true;


        if(md5(md5($token + "GJSK&")) != $email)
        {
            return false;
        }
        else return true;
    }

    //仅用于测试
    public static function clearTable($table_name)
    {
        $db = new mysqli(CONFIG::$db['host'], CONFIG::$db['user'], CONFIG::$db['pwd'], CONFIG::$db['dbname']);
        if($db->connect_error)
            return false;
        $sql = 'DELETE FROM '.$table_name;
        $db->query($sql);
        $db->close();
        return true;
    }
}




?>