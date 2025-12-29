import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext();

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for saved user in localStorage
    const savedUser = localStorage.getItem('safecircle_user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const result = await api.login(email, password);
      const { access_token, user: foundUser } = result;
      localStorage.setItem('safecircle_token', access_token);
      localStorage.setItem('safecircle_user', JSON.stringify(foundUser));
      setUser(foundUser);
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.message };
    }
  };

  const signup = async (userData) => {
    try {
      const result = await api.signup(userData);
      const { access_token, user: createdUser } = result;
      localStorage.setItem('safecircle_token', access_token);
      localStorage.setItem('safecircle_user', JSON.stringify(createdUser));
      setUser(createdUser);
      return { success: true };
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('safecircle_user');
    localStorage.removeItem('safecircle_token');
    setUser(null);
  };

  const updateUser = async (updates) => {
    try {
      const updatedUser = await api.updateUser(user.id, updates);
      localStorage.setItem('safecircle_user', JSON.stringify(updatedUser));
      setUser(updatedUser);
      return { success: true };
    } catch (error) {
      console.error('Update user error:', error);
      return { success: false, error: error.message };
    }
  };

  const completeProfile = async (profileData) => {
    try {
      const updatedUser = await api.updateUser(user.id, {
        ...profileData,
        profileComplete: true
      });
      localStorage.setItem('safecircle_user', JSON.stringify(updatedUser));
      setUser(updatedUser);
      return { success: true };
    } catch (error) {
      console.error('Complete profile error:', error);
      return { success: false, error: error.message };
    }
  };

  const value = {
    user,
    loading,
    login,
    signup,
    logout,
    updateUser,
    completeProfile
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
