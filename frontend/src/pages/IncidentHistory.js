import React, { useState, useEffect } from 'react';
import { BottomNav } from '../components/BottomNav';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Calendar, MapPin, Clock, Star, TrendingUp } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { motion } from 'framer-motion';

export default function IncidentHistory() {
  const { user } = useAuth();
  const [filter, setFilter] = useState('all');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
       try {
          const incidents = await api.getIncidents();
          const myHistory = incidents.filter(inc => 
             inc.victim?.id === user?.id || inc.respondingHelpers?.includes(user?.id)
          ).map(inc => ({
             ...inc,
             role: inc.victim?.id === user?.id ? 'victim' : 'helper'
          }));
          setHistory(myHistory);
       } catch (e) {
          console.error("Failed to fetch history", e);
       } finally {
          setLoading(false);
       }
    };
    if (user) fetchHistory();
  }, [user]);
  
  const typeColors = {
    Medical: 'bg-destructive text-destructive-foreground',
    Assault: 'bg-warning text-warning-foreground',
    Accident: 'bg-secondary text-secondary-foreground',
    Other: 'bg-muted text-muted-foreground'
  };
  
  const filteredHistory = history.filter(h => {
    if (filter === 'all') return true;
    return h.role === filter;
  });

  const totalIncidents = history.length;
  const asVictim = history.filter(h => h.role === 'victim').length;
  const asHelperIncidents = history.filter(h => h.role === 'helper');
  const asHelper = asHelperIncidents.length;
  
  // Calculate average response time
  let totalResponseTime = 0;
  let responseCount = 0;
  
  asHelperIncidents.forEach(inc => {
    if (inc.chatMessages && inc.chatMessages.length > 0) {
       // Find first message from me
       const myFirstMsg = inc.chatMessages
         .filter(m => m.sender === user?.id)
         .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))[0];
         
       if (myFirstMsg) {
          const incidentTime = new Date(inc.timestamp);
          const msgTime = new Date(myFirstMsg.timestamp);
          const diffInMinutes = (msgTime - incidentTime) / (1000 * 60);
          if (diffInMinutes > 0) {
             totalResponseTime += diffInMinutes;
             responseCount++;
          }
       }
    }
  });
  
  const avgResponseTime = responseCount > 0 
    ? Math.round(totalResponseTime / responseCount) + ' min' 
    : 'N/A';
  
  return (
    <div className="min-h-screen bg-background pb-20">
      <header className="bg-card border-b border-border">
        <div className="max-w-screen-xl mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold mb-1">Incident History</h1>
          <p className="text-sm text-muted-foreground">Your past emergencies and responses</p>
          
          <Tabs value={filter} onValueChange={setFilter} className="mt-4">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="all">All</TabsTrigger>
              <TabsTrigger value="victim">As Victim</TabsTrigger>
              <TabsTrigger value="helper">As Helper</TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </header>
      
      <main className="max-w-screen-xl mx-auto px-4 py-6">
        {/* Statistics Summary */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
          <Card>
            <CardContent className="p-4 text-center">
              <p className="text-2xl font-bold">{totalIncidents}</p>
              <p className="text-xs text-muted-foreground">Total Incidents</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <p className="text-2xl font-bold">{asVictim}</p>
              <p className="text-xs text-muted-foreground">As Victim</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <p className="text-2xl font-bold">{asHelper}</p>
              <p className="text-xs text-muted-foreground">As Helper</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <p className="text-2xl font-bold">{avgResponseTime}</p>
              <p className="text-xs text-muted-foreground">Avg Response</p>
            </CardContent>
          </Card>
        </div>
        
        {/* History List */}
        {loading ? (
            <div className="text-center py-8">Loading history...</div>
        ) : (
        <div className="space-y-3">
          {filteredHistory.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">No incidents found.</div>
          ) : (
          filteredHistory.map((incident, index) => (
            <motion.div
              key={incident.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card className="hover:shadow-medium transition-shadow cursor-pointer">
                <CardContent className="p-4">
                  <div className="flex items-start gap-3">
                    {incident.role === 'helper' && incident.victim ? (
                      <Avatar className="h-12 w-12">
                        <AvatarImage src={incident.victim.profilePic} alt={incident.victim.name} />
                        <AvatarFallback>{incident.victim.name[0]}</AvatarFallback>
                      </Avatar>
                    ) : (
                      <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                        <span className="text-xl">🆘</span>
                      </div>
                    )}
                    
                    <div className="flex-1">
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <div>
                          <h3 className="font-semibold">
                            {incident.role === 'helper' ? `Helped ${incident.victim?.name || 'Someone'}` : 'Emergency Alert'}
                          </h3>
                          <p className="text-xs text-muted-foreground flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {incident.timestamp ? formatDistanceToNow(new Date(incident.timestamp)) : 'Unknown time'} ago
                          </p>
                        </div>
                        <Badge className={typeColors[incident.type] || typeColors.Other}>
                          {incident.type}
                        </Badge>
                      </div>
                      
                      <div className="flex items-center gap-1 text-sm text-muted-foreground mb-2">
                        <MapPin className="h-3 w-3" />
                        {incident.locationName || 'Unknown Location'}
                      </div>
                      
                      {incident.role === 'helper' && (
                        <div className="flex items-center gap-1 text-xs text-yellow-600 bg-yellow-50 px-2 py-1 rounded-full w-fit">
                          <Star className="h-3 w-3 fill-yellow-600" />
                          +50 points earned
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))
          )}
        </div>
        )}
      </main>
      
      <BottomNav />
    </div>
  );
}
