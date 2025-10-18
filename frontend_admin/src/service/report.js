import axios from '../utils/axios';

// 获取所有举报
export function getAllReports() {
    return axios.get('/report/all', {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    });
}

// 处理举报
export function reviewReport(reportId, status) {
    return axios.post(
        `/report/review/${reportId}`,
        { status }, // 请求体
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
    );
}
