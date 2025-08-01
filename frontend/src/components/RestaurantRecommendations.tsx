import React from 'react';
import { RestaurantCard } from './RestaurantCard';
import { UserData } from '../services/authService';
import { motion } from 'framer-motion';

interface Restaurant {
  id: string;
  name: string;
  image_url?: string;
  rating?: number;
  address?: string;
  phone?: string;
  website?: string;
  cuisine_type?: string;
  price_range?: string;
  description?: string;
}

interface RestaurantRecommendationsProps {
  restaurants: Restaurant[];
  sessionId: string;
  userData: UserData;
  isHistoryView?: boolean;
}

export const RestaurantRecommendations: React.FC<RestaurantRecommendationsProps> = ({ 
  restaurants, 
  sessionId,
  userData,
  isHistoryView = false
}) => {
  const handlePreferenceSaved = (restaurantId: string, preference: 'like' | 'dislike') => {
    console.log(`User ${preference}d restaurant ${restaurantId}`);
    // Additional logic can be added here, like showing a toast notification
  };

  if (!restaurants || restaurants.length === 0) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mt-4 w-full"
    >
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">
          🍽️ {isHistoryView ? 'Restaurant Recommendations (From History)' : 'Restaurant Recommendations'}
        </h3>
        <p className="text-sm text-gray-600">
          {isHistoryView 
            ? 'These were the restaurants recommended in this conversation.'
            : 'Here are some great options I found for you. Use the like/dislike buttons to help me learn your preferences!'
          }
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
        {restaurants.map((restaurant, index) => (
          <motion.div
            key={restaurant.id}
            className="w-full flex flex-col h-full"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="flex-grow flex flex-col h-full">
              <RestaurantCard
                restaurant={restaurant}
                sessionId={sessionId}
                userData={userData}
                onPreferenceSaved={handlePreferenceSaved}
                isHistoryView={isHistoryView}
              />
            </div>
          </motion.div>

        ))}
      </div>
    </motion.div>
  );
};
