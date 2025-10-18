// src/services/messageService.js
import { socket } from './chatService';
import { setPrivateUnreadHandler, setGroupUnreadHandler } from './chatService';

/**
 * 注册私聊未读消息处理函数
 * @param {Function} handler - 处理函数(data)
 */
export const registerPrivateUnreadHandler = (handler) => {
    setPrivateUnreadHandler(handler);
};

/**
 * 注册群聊未读消息处理函数
 * @param {Function} handler - 处理函数(data)
 */
export const registerGroupUnreadHandler = (handler) => {
    setGroupUnreadHandler(handler);
};

/**
 * 获取私聊未读消息数量
 * @param {string} token - 用户的 JWT token
 * @returns {Promise<Object>}
 * 未用到
 */
export const getPrivateUnreadCount = (token) => {
    return new Promise((resolve, reject) => {
        if (!token) {
            console.error('Token is required to fetch private unread messages');
            reject(new Error('Token is required'));
            return;
        }
        socket?.emit('private_unread', { token }, (ack) => {
            if (ack?.error) {
                console.error('Failed to get private unread message count:', ack.error);
                reject(new Error(ack.error));
            } else {
                console.log('Private unread message count fetched successfully');
                resolve(ack);
            }
        });
    });
};

/**
 * 获取群聊未读消息数量
 * @param {string} token - 用户的 JWT token
 * @returns {Promise<Object>}
 * 未用到
 */
export const getGroupUnreadCount = (token) => {
    return new Promise((resolve, reject) => {
        if (!token) {
            console.error('Token is required to fetch group unread messages');
            reject(new Error('Token is required'));
            return;
        }
        socket?.emit('group_unread', { token }, (ack) => {
            if (ack?.error) {
                console.error('Failed to get group unread message count:', ack.error);
                reject(new Error(ack.error));
            } else {
                console.log('Group unread message count fetched successfully');
                resolve(ack);
            }
        });
    });
};

/**
 * 将私聊消息标记为已读
 * @param {string} token - 用户的 JWT token
 * @param {string} sender_id - 发件人 ID
 * @returns {Promise<void>}
 */
export const markPrivateMessagesAsRead = (token, sender_id) => {
    return new Promise((resolve, reject) => {
        console.log('markPrivateMessagesAsRead');
        if (!token || !sender_id) {
            console.error('Token and sender_id are required to mark messages as read');
            reject(new Error('Token and sender_id are required'));
            return;
        }
        socket?.emit('private_read', { token, sender_id }, (ack) => {
            if (ack?.error) {
                console.error('Failed to mark private messages as read:', ack.error);
                reject(new Error(ack.error));
            } else {
                console.log('Private messages marked as read successfully');
                resolve();
            }
        });
    });
};

/**
 * 将群聊消息标记为已读
 * @param {string} token - 用户的 JWT token
 * @param {string} group_id - 群组 ID
 * @returns {Promise<void>}
 */
export const markGroupMessagesAsRead = (token, group_id) => {
    return new Promise((resolve, reject) => {
        if (!token || !group_id) {
            console.error('Token and group_id are required to mark messages as read');
            reject(new Error('Token and group_id are required'));
            return;
        }
        socket?.emit('group_read', { token, group_id }, (ack) => {
            if (ack?.error) {
                console.error('Failed to mark group messages as read:', ack.error);
                reject(new Error(ack.error));
            } else {
                console.log('Group messages marked as read successfully');
                resolve();
            }
        });
    });
};
