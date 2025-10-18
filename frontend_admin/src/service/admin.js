import axios from '../utils/axios'

export function getAdminInfo() {
    return axios.get('/admin/profile',
        {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
          }
    );
}

export function adminLogout() {  
    return axios.post('/admin/logout',{},
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
    );
}

export function getUser() {
    return axios.get('/admin/users',
        {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
    );
}

export function banUser(userId) {
    return axios.patch(
        `/admin/users/${userId}/forbid`,
        {}, // No body, so an empty object
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
    );
}

export function unbanUser(userId) {
    return axios.patch(
        `/admin/users/${userId}/unforbid`,
        {}, // No body, so an empty object
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
    );
}

export function deleteUser(userId) {
    return axios.delete(`/admin/users/${userId}/delete`,
        {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
    );
}
