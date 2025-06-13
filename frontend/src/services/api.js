const API_BASE_URL = 'http://localhost:5000';

export const api = {
  getDocuments: async (page = 1, perPage = 10) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/documents?page=${page}&per_page=${perPage}`);
      if (!response.ok) {
        const errorText = await response.text();
        console.error('API response error:', errorText);
        throw new Error('Failed to fetch documents');
      }
      return await response.json();
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  },
  
  getDocument: async (docId) => {
    try {
      console.log('Fetching document with ID:', docId);
      const response = await fetch(`${API_BASE_URL}/api/document/${encodeURIComponent(docId)}`);
      if (!response.ok) {
        const errorText = await response.text();
        console.error('API response error:', errorText);
        throw new Error('Failed to fetch document');
      }
      return await response.json();
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  },
  
  getSimilarDocuments: async (docId, topK = 5) => {
    try {
      console.log(`Fetching similar documents for ID: ${docId} with top-k=${topK}`);
      const response = await fetch(`${API_BASE_URL}/api/similar/${encodeURIComponent(docId)}?top_k=${topK}`);
      if (!response.ok) {
        const errorText = await response.text();
        console.error('API response error:', errorText);
        throw new Error('Failed to fetch similar documents');
      }
      return await response.json();
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  },
  
  search: async (query, topK = 10) => {
    try {
      console.log(`Searching for "${query}" with top-k=${topK}`);
      const response = await fetch(`${API_BASE_URL}/api/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query,
          top_k: topK
        }),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('API response error:', errorText);
        throw new Error('Search failed');
      }
      
      const data = await response.json();
      console.log('Search API response:', data);
      return data;
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  }
};