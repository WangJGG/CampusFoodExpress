// group.js

import axios from '../utils/axios';

// 获取群聊信息和成员列表
export const  getGroup  = async (group_id) => {
  return axios.get('/eatinggroup/get_group_by_groupid', {
      params: { group_id: group_id },
      headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
  });
};

export const updateGroup = async (groupData) => {
return axios.post('/eatinggroup/update_group', groupData, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`,  // 从localStorage获取JWT Token
  }
});
};

export const deleteGroupMember = async (memberId) => {
return axios.delete('/eatinggroup/delete_member_by_memberid', {
  data: { id: memberId },  // 传递要删除的成员 ID
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`,  // 从localStorage获取JWT Token
  }
});
};

// 调用后端删除群聊接口
export const deleteGroup = async (groupId) => {
return axios.delete('/eatinggroup/delete_group', {
  params: { group_id: groupId },  // 传递要删除的群聊 ID
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`,  // 从localStorage获取JWT Token
  }
});
};


// 请求群聊列表
export const fetchGroupChats = async () => {
  try {
    const response = await axios.get('/eatinggroup/get_group_by_userid');  // 假设群聊接口为 /api/groupChats
    console.log('get_group_by_userid response:', response.data.groups.length);
    if (response.data.groups.length > 0) {
      console.log('success:', response.data.groups);
      return response.data;  // 返回群聊数据
    // } else {
    //   console.error('获取群聊数据失败:', response.data.message);
    //   return [];
    }
  } catch (error) {
    console.error('请求群聊列表失败:', error);
    return [];
  }
};

// 创建群聊
export const createGroup = async (selectedFriends) => {
  if (selectedFriends.length === 0) {
    throw new Error('请至少选择一个好友');
  }

  const groupData = {
    name: "未命名",  // 默认群聊名称
    description: "  ",  // 默认群聊描述
    member_user_ids: selectedFriends  // 选中的好友 ID
  };

  try {
    const response = await axios.post('/eatinggroup/add_group', groupData);

    if (response.data && response.data.message === 'Group added successfully') {
      const group = response.data.group;  // 获取创建成功的群聊信息
      const owner = response.data.owner;  // 获取群主信息
      return { group, owner };
    } else {
      throw new Error(response.data.error || '创建群聊失败');
    }
  } catch (error) {
    throw new Error(error.response?.data?.error || '请求失败，请检查网络连接');
  }
};


// 添加群成员
export const addMember = async (groupId, userId) => {
  if (!groupId || !userId) {
    throw new Error('群聊ID和用户ID不能为空');
  }

  const memberData = {
    group_id: groupId,
    user_id: userId
  };

  try {
    const response = await axios.post('/eatinggroup/add_member', memberData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('jwt_token')}`  // 假设JWT Token存储在localStorage中
      }
    });

    if (response.data && response.data.message === 'Member added successfully') {
      const member = response.data.member;  // 获取成功添加的成员信息
      return member;
    } else {
      throw new Error(response.data.error || '添加成员失败');
    }
  } catch (error) {
    throw new Error(error.response?.data?.error || '请求失败，请检查网络连接');
  }
};
