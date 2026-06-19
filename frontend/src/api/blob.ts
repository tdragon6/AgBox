import { getToken } from '@/utils/auth';

export default async function apiGetBlobUrl(url: string, isDownload = false) {
  const baseURL = import.meta.env.VITE_API_BASE_URL;
  const token = getToken();
  const headers: Record<string, string> = {};
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  const response = await fetch(`${baseURL}${url}`, { headers });
  const blob = await response.blob();

  const blobUrl = URL.createObjectURL(blob);

  if (isDownload === true) {
    const contentDisposition = response.headers.get('Content-Disposition');
    const fileName = contentDisposition?.split('filename=')[1] as string;

    const a = document.createElement('a');
    a.href = blobUrl;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(blobUrl);
  }

  return blobUrl;
}
