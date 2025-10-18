import axios from '../utils/axios'

export function getMarkers() {
  return axios.get('/restaurant/marker',
    {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
    }
  );
}
