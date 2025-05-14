import { useEffect } from 'react';
import { useLocation } from 'react-router';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';

NProgress.configure({ showSpinner: false });

export const useRouteProgress = () => {
  const location = useLocation();

  useEffect(() => {
    NProgress.start();
    // Simulate delay or wait for fetch if needed
    const timer = setTimeout(() => {
      NProgress.done();
    }, 300); // delay to avoid flicker

    return () => {
      clearTimeout(timer);
    };
  }, [location]);
};
