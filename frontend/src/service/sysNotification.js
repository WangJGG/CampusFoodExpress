import axios from '../utils/axios';



// 获取最新一条系统消息
export const getLatestNotification = async () => {
  try {
    const response = await axios.get('/system_notification/get_latest_notification_by_user_id');
    return response.data.notification; // 返回最新消息
  } catch (error) {
    console.error('Error fetching the latest notification:', error);
    throw error; // 抛出错误以便调用方处理
  }
};

// 检查是否有新消息（获取未读消息数量）
export const getUnreadNotificationsCount = async () => {
  try {
    const response = await axios.get('/system_notification/get_unread_notifications_count');
    return response.data.unread_num; // 返回未读消息数量
  } catch (error) {
    console.error('Error fetching unread notifications count:', error);
    throw error; // 抛出错误以便调用方处理
  }
};

// 获取所有系统消息
export const getAllNotifications = async () => {
  try {
    const response = await axios.get('/system_notification/get_all_notification_by_user_id');
    return response.data.notifications; // 返回所有消息数据
  } catch (error) {
    console.error('Error fetching all notifications:', error);
    throw error; // 抛出错误以便调用方处理
  }
};


// 更新所有系统消息的已读状态
export const updateAllNotificationStatus = async () => {
  try {
    const response = await axios.put('/system_notification/update_all_system_notification_status', null, {});
    return response.data.message; // 返回成功消息
  } catch (error) {
    console.error('Error updating notification status:', error);
    throw error; // 抛出错误以便调用方处理
  }
};

