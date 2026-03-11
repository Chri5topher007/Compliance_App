import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import PrivateRoute from './components/PrivateRoute';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import DepartmentDashboard from './components/DepartmentDashboard';
import AuditScheduler from './components/AuditScheduler';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Switch>
          <Route path="/login" component={Login} />
          <PrivateRoute exact path="/" component={Dashboard} />
          <PrivateRoute path="/department" component={DepartmentDashboard} />
          <PrivateRoute path="/scheduler" component={AuditScheduler} />
        </Switch>
      </Router>
    </AuthProvider>
  );
}
export default App;