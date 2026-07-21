import { useEffect, useState } from 'react';
import { fetchJson } from '@/lib/api';

export function useInsights<T>(path: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchJson<T>(path)
      .then((result) => setData(result))
      .catch(() => setError('Unable to load data'))
      .finally(() => setLoading(false));
  }, [path]);

  return { data, loading, error };
}
