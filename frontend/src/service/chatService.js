// src/services/chatService.js
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { io } from 'socket.io-client';
const API_URL = 'http://127.0.0.1:5000/api/chat'; // 后端 API URL
export let socket = null; // 导出 WebSocket 实例
// 处理函数
let _privateUnreadHandler = null;
let _groupUnreadHandler = null;

export const setPrivateUnreadHandler = (handler) => {
    _privateUnreadHandler = handler;
};

export const setGroupUnreadHandler = (handler) => {
    _groupUnreadHandler = handler;
};

export const getPrivateUnreadHandler = () => _privateUnreadHandler;
export const getGroupUnreadHandler = () => _groupUnreadHandler;

let privateMessageHandler = null;
let groupMessageHandler = null;

/**
 * 注册 WebSocket 事件监听器
 */
const registerEventListeners = () => {
    if (!socket) return;

    // 清理旧监听器，避免重复触发
    socket.off('private_message');
    socket.off('group_message');
    socket.off('private_unread');
    socket.off('group_unread');
    socket.off('private_read');
    socket.off('group_read');

    // 注册私聊未读消息监听器
    socket.on('private_unread', (data) => {
        console.log('Private unread message count:', data);
        _privateUnreadHandler?.(data);
    });

    // 注册群聊未读消息监听器
    socket.on('group_unread', (data) => {
        console.log('Group unread message count:', data);
        _groupUnreadHandler?.(data);
    });

    // 注册私聊已读消息响应
    socket.on('private_read', (data) => {
        console.log('Private messages marked as read:', data);
    });

    // 注册群聊已读消息响应
    socket.on('group_read', (data) => {
        console.log('Group messages marked as read:', data);
    });

    // 注册私聊消息监听器
    socket.on('private_message', (message) => {
        console.log('Private message received:', message);
        if(message.status === 'error') {
            ElMessage.error(message.error);
            return;
        }
        privateMessageHandler?.(message, false);
    });

    // 注册群聊消息监听器
    socket.on('group_message', (message) => {
        console.log('Group message received:', message);
        if(message.status === 'error') {
            ElMessage.error(message.error);
            return;
        }
        groupMessageHandler?.(message, true);
        console.log(groupMessageHandler);
    });
};

/**
 * 初始化 WebSocket 连接
 * @param {string} token - 用户的 JWT token
 */
export const connectSocket = (token) => {
    if (!token) {
        console.error('Token is missing');
        return;
    }

    if (socket?.connected) {
        console.log('WebSocket is already connected');
        return;
    }

    try {
        socket = io('http://127.0.0.1:5000', {
            auth: { token },
            // transports: ['websocket'],
            timeout: 300000,
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000,
        });

        // 注册事件监听器
        registerEventListeners();

        socket.on('connect', () => {
            console.log('Connected to WebSocket');
            socket.emit('join_room', { token });
        });

        socket.on('disconnect', () => console.log('Disconnected from WebSocket'));
        socket.on('connect_error', (error) => console.error('WebSocket connection error:', error));
        socket.on('reconnect_attempt', (attempt) => console.log(`Reconnect attempt #${attempt}`));
        socket.on('reconnect_failed', () => console.error('WebSocket reconnection failed'));
    } catch (error) {
        console.error('Error initializing WebSocket:', error);
    }
};

/**
 * 断开 WebSocket 连接
 */
export const disconnectSocket = (token) => {
    if (socket) {
        socket.emit('leave_room', { token });
        socket.removeAllListeners();
        socket.disconnect();
        console.log('WebSocket disconnected');
        socket = null;
    }
};

/**
 * 注册私聊消息处理函数
 * @param {Function} handler - 处理函数(message, isGroup)
 */
export const registerPrivateMessageHandler = (handler) => {
    privateMessageHandler = handler;
};

/**
 * 注册群聊消息处理函数
 * @param {Function} handler - 处理函数(message, isGroup)
 */
export const registerGroupMessageHandler = (handler) => {
    groupMessageHandler = handler;
};

/**
 * 发送私聊消息
 * @param {string} token - 用户的 JWT token
 * @param {string} receiver_id - 接收者 ID
 * @param {string} content - 消息内容
 * @param {string} content_type - 消息类型（默认 'text'）
 * @returns {Promise<void>}
 */
export const sendPrivateMessage = (token, receiver_id, content, content_type = 'text') => {
    return new Promise((resolve, reject) => {
        if (!receiver_id || !content) {
            console.error('Receiver ID and content are required for private messages');
            reject(new Error('Receiver ID and content are required'));
            return;
        }
        const message = { receiver_id, content, content_type };
        socket?.emit('private_message', { message, token }, (ack) => {
            if (ack?.status === 'error') {
                console.error('Failed to send private message:', ack.error);
                reject(new Error(ack.error));
            } else {
                console.log('Private message sent successfully');
                resolve();
            }
        });
    });
};

/**
 * 发送群聊消息
 * @param {string} token - 用户的 JWT token
 * @param {string} group_id - 群组 ID
 * @param {string} content - 消息内容
 * @param {string} content_type - 消息类型（默认 'text'）
 * @returns {Promise<void>}
 */
export const sendGroupMessage = (token, group_id, content, content_type = 'text') => {
    return new Promise((resolve, reject) => {
        if (!group_id || !content) {
            console.error('Group ID and content are required for group messages');
            reject(new Error('Group ID and content are required'));
            return;
        }
        const message = { group_id, content, content_type };
        socket?.emit('group_message', { message, token }, (ack) => {
            if (ack?.status === 'error') {
                console.error('Failed to send group message:', ack.error);
                reject(new Error(ack.error));
            } else {
                console.log('Group message sent successfully');
                resolve();
            }
        });
    });
};

/**
 * 获取消息历史
 * @param {string|null} receiver_id - 私聊目标用户 ID
 * @param {string|null} group_id - 群聊 ID
 * @param {number} page - 当前页码
 * @param {number} per_page - 每页消息数量
 * @returns {Promise<Object>} 消息历史数据
 */
export const getMessageHistory = async (receiver_id = null, group_id = null, page = 1, per_page = 20) => {
    const token = localStorage.getItem('token');
    if (!token) {
        console.error('Token is required to fetch message history');
        throw new Error('Token is required to fetch message history');
    }

    if (!receiver_id && !group_id) {
        console.error('Either receiver_id or group_id must be provided');
        throw new Error('Either receiver_id or group_id must be provided');
    }

    try {
        const response = await axios.get(`${API_URL}/get_history`, {
            headers: { Authorization: `Bearer ${token}` },
            params: { receiver_id, group_id, page, per_page },
        });

        console.log('Message history fetched successfully');
        return response.data;
    } catch (error) {
        console.error('Error fetching message history:', error.response?.data || error.message);
        throw error;
    }
};
