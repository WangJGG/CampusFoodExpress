import axios from '../utils/axios'

export function get_authenticate() {
    return axios.get('auth/all_verification_requests',
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
    );
}

// 更新实名认证审核请求
export function update_authenticate(params) {
    return axios.post(`auth/review_verification/${params.id}`,
        { status: params.status }, // 请求体只发送审核状态
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            }
        }
    )
}
