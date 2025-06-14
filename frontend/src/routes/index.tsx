import React from 'react';
import { createBrowserRouter, Outlet, type RouteObject } from 'react-router-dom';
import { Home, Options, ProgressLog } from '../pages';

const MainLayout: React.FC = () => (
    <Outlet />
);

const routes: RouteObject[] = [
    {
        path: '/',
        element: <MainLayout />, 
        children: [
            { index: true, element: <Home /> },
            { path: 'log', element: <ProgressLog /> },
            { path: 'options', element: <Options /> },
            { path: '*', element: <Home /> }
        ]
    }
];

const router = createBrowserRouter(routes);
export default router;