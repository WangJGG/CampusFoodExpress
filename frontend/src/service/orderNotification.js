import axios from '../utils/axios';


/**
 * 获取用户的最新订单消息
 * @returns {Promise<object>} 最新订单消息数据
 */
export const getLatestOrderNotification = async () => {
  try {
    const response = await axios.get('/order_notification/get_latest_notification_by_user_id');
    console.log(response.data.notification);
    return response.data.notification; // 返回最新的订单消息
  } catch (error) {
    console.error('Error fetching latest order notification:', error);
    throw error; // 抛出错误以便调用方处理
  }
};

/**
 * 获取所有订单消息
 * @returns {Promise<Array>} 所有订单消息的数组
 */
export const getAllOrderNotifications = async () => {
  try {
    const response = await axios.get('/order_notification/get_all_notifications_by_user_id');
    return response.data.notifications; // 返回所有订单消息
  } catch (error) {
    console.error('Error fetching all order notifications:', error);
    throw error; // 抛出错误以便调用方处理
  }
};

/**
 * 获取未读订单消息数量
 * @returns {Promise<number>} 未读消息数量
 */
export const getUnreadOrderNotificationsCount = async () => {
  try {
    const response = await axios.get('/order_notification/get_unread_notifications_count');
    return response.data.unread_num; // 返回未读消息数量
  } catch (error) {
    console.error('Error fetching unread order notifications count:', error);
    throw error; // 抛出错误以便调用方处理
  }
};

/**
 * 更新指定订单消息的已读状态

 */
export const updateAllOrderNotificationsStatus = async () => {
  try {
    const response = await axios.put('/order_notification/update_all_order_notifications_status', null);
    return response.data.message; // 返回成功消息
  } catch (error) {
    console.error('Error updating all order notification statuses:', error);
    throw error; // 抛出错误以便调用方处理
  }
};
