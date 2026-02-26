import { useState, useEffect } from 'react';
import { 
  Dumbbell, 
  Menu, 
  X, 
  ChevronRight, 
  Users, 
  Award, 
  Clock, 
  MapPin, 
  Phone, 
  Mail, 
  Instagram, 
  Facebook, 
  Twitter, 
  Check,
  Flame,
  Heart,
  Zap,
  Utensils,
  Calendar,
  ArrowRight,
  Star
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { toast } from 'sonner';
import './App.css';

// Types
interface Program {
  id: string;
  title: string;
  description: string;
  image: string;
  duration: string;
  level: string;
  calories: string;
}

interface Membership {
  id: string;
  name: string;
  description: string;
  priceMonthly: number;
  priceYearly: number;
  features: string[];
  notIncluded: string[];
  popular?: boolean;
}

interface Trainer {
  id: string;
  name: string;
  role: string;
  image: string;
  experience: string;
  specialization: string[];
}

interface MealPlan {
  id: string;
  title: string;
  description: string;
  category: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  image: string;
  meals: { name: string; time: string; description: string; calories: number }[];
}

interface Testimonial {
  id: string;
  name: string;
  role: string;
  content: string;
  rating: number;
  image: string;
}

// Data
const programs: Program[] = [
  {
    id: '1',
    title: 'HIIT Training',
    description: 'High-Intensity Interval Training that burns calories and builds endurance through explosive workouts.',
    image: '/program-hiit.jpg',
    duration: '45 min',
    level: 'Advanced',
    calories: '500-700'
  },
  {
    id: '2',
    title: 'Yoga & Meditation',
    description: 'Find your inner peace with our expert-led yoga sessions designed for all skill levels.',
    image: '/program-yoga.jpg',
    duration: '60 min',
    level: 'All Levels',
    calories: '200-300'
  },
  {
    id: '3',
    title: 'Strength Training',
    description: 'Build muscle and increase power with our comprehensive strength training programs.',
    image: '/program-strength.jpg',
    duration: '50 min',
    level: 'Intermediate',
    calories: '400-600'
  },
  {
    id: '4',
    title: 'Cardio Blast',
    description: 'Improve your cardiovascular health with dynamic cardio workouts and state-of-the-art equipment.',
    image: '/program-cardio.jpg',
    duration: '40 min',
    level: 'All Levels',
    calories: '350-500'
  }
];

const memberships: Membership[] = [
  {
    id: 'basic',
    name: 'Basic',
    description: 'Essential access to gym facilities',
    priceMonthly: 2499,
    priceYearly: 24999,
    features: [
      'Access to gym equipment',
      'Locker room access',
      'Free WiFi',
      'Fitness assessment',
      'Mobile app access'
    ],
    notIncluded: ['Group classes', 'Personal training', 'Nutrition consultation']
  },
  {
    id: 'premium',
    name: 'Premium',
    description: 'Full access with additional perks',
    priceMonthly: 3999,
    priceYearly: 39999,
    features: [
      'Access to gym equipment',
      'Locker room access',
      'Free WiFi',
      'Fitness assessment',
      'Mobile app access',
      'Unlimited group classes',
      '2 personal training sessions/month',
      'Towel service'
    ],
    notIncluded: ['Nutrition consultation', 'Guest passes'],
    popular: true
  },
  {
    id: 'elite',
    name: 'Elite',
    description: 'The ultimate fitness experience',
    priceMonthly: 5999,
    priceYearly: 59999,
    features: [
      'Access to gym equipment',
      'Locker room access',
      'Free WiFi',
      'Fitness assessment',
      'Mobile app access',
      'Unlimited group classes',
      '4 personal training sessions/month',
      'Towel service',
      'Nutrition consultation',
      '4 guest passes/month',
      'Priority class booking',
      'Recovery spa access'
    ],
    notIncluded: []
  }
];

const trainers: Trainer[] = [
  {
    id: '1',
    name: 'Arjun Sharma',
    role: 'Head Strength Coach',
    image: '/trainer-1.jpg',
    experience: '10+ years',
    specialization: ['Strength Training', 'Powerlifting', 'Bodybuilding']
  },
  {
    id: '2',
    name: 'Priya Patel',
    role: 'HIIT Specialist',
    image: '/trainer-2.jpg',
    experience: '8 years',
    specialization: ['HIIT', 'Cardio', 'Weight Loss']
  },
  {
    id: '3',
    name: 'Rahul Kumar',
    role: 'Yoga Master',
    image: '/trainer-3.jpg',
    experience: '15 years',
    specialization: ['Yoga', 'Meditation', 'Mindfulness']
  },
  {
    id: '4',
    name: 'Dr. Ananya Reddy',
    role: 'Nutritionist',
    image: '/trainer-4.jpg',
    experience: '12 years',
    specialization: ['Nutrition', 'Diet Planning', 'Wellness']
  }
];

const mealPlans: MealPlan[] = [
  {
    id: '1',
    title: 'Weight Loss Plan',
    description: 'A calorie-deficit meal plan designed to promote healthy weight loss with Indian cuisine options.',
    category: 'weight_loss',
    calories: 1800,
    protein: 40,
    carbs: 30,
    fat: 30,
    image: '/meal-healthy.jpg',
    meals: [
      { name: 'Breakfast', time: '8:00 AM', description: 'Vegetable oats upma with sprouts', calories: 300 },
      { name: 'Lunch', time: '12:30 PM', description: 'Roti with paneer bhurji and cucumber raita', calories: 450 },
      { name: 'Snack', time: '3:30 PM', description: 'Roasted chana with a small apple', calories: 200 },
      { name: 'Dinner', time: '7:00 PM', description: 'Grilled fish with steamed brown rice', calories: 550 }
    ]
  },
  {
    id: '2',
    title: 'Muscle Gain Plan',
    description: 'A protein-rich meal plan designed to support muscle growth and recovery.',
    category: 'muscle_gain',
    calories: 3000,
    protein: 35,
    carbs: 45,
    fat: 20,
    image: '/meal-healthy.jpg',
    meals: [
      { name: 'Breakfast', time: '7:00 AM', description: 'Protein oatmeal with banana and peanut butter', calories: 500 },
      { name: 'Mid-Morning', time: '10:00 AM', description: 'Protein shake with almonds', calories: 350 },
      { name: 'Lunch', time: '1:00 PM', description: 'Grilled chicken with brown rice and vegetables', calories: 700 },
      { name: 'Dinner', time: '8:00 PM', description: 'Salmon with quinoa and roasted veggies', calories: 650 }
    ]
  },
  {
    id: '3',
    title: 'Vegetarian Plan',
    description: 'A plant-based meal plan rich in nutrients and protein alternatives.',
    category: 'vegetarian',
    calories: 2200,
    protein: 25,
    carbs: 50,
    fat: 25,
    image: '/meal-healthy.jpg',
    meals: [
      { name: 'Breakfast', time: '8:00 AM', description: 'Paneer bhurji with whole grain toast', calories: 400 },
      { name: 'Lunch', time: '12:30 PM', description: 'Dal tadka with brown rice and salad', calories: 500 },
      { name: 'Snack', time: '3:30 PM', description: 'Hummus with carrot and cucumber sticks', calories: 250 },
      { name: 'Dinner', time: '7:30 PM', description: 'Tofu curry with quinoa', calories: 450 }
    ]
  }
];

const testimonials: Testimonial[] = [
  {
    id: '1',
    name: 'Vikram Mehta',
    role: 'Software Engineer',
    content: 'The Fitness Revolution transformed my life. I lost 15kg in 6 months with their personalized training and nutrition plans.',
    rating: 5,
    image: '/trainer-1.jpg'
  },
  {
    id: '2',
    name: 'Sneha Gupta',
    role: 'Marketing Manager',
    content: 'Best gym in Bangalore! The trainers are knowledgeable and the facilities are world-class. Highly recommend!',
    rating: 5,
    image: '/trainer-2.jpg'
  },
  {
    id: '3',
    name: 'Karthik Iyer',
    role: 'Business Owner',
    content: 'The mental wellness programs here are exceptional. Yoga and meditation sessions have helped me manage stress effectively.',
    rating: 5,
    image: '/trainer-3.jpg'
  }
];

// Components
function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: 'Home', href: '#home' },
    { name: 'About', href: '#about' },
    { name: 'Programs', href: '#programs' },
    { name: 'Membership', href: '#membership' },
    { name: 'Trainers', href: '#trainers' },
    { name: 'Meal Plans', href: '#meal-plans' },
    { name: 'Contact', href: '#contact' }
  ];

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-black/95 backdrop-blur-md shadow-lg' : 'bg-transparent'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          <a href="#home" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center">
              <Dumbbell className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-white">Fitness Revolution</span>
          </a>
          
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                className="text-gray-300 hover:text-orange-500 transition-colors font-medium"
              >
                {link.name}
              </a>
            ))}
            <Button className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white">
              Join Now
            </Button>
          </div>

          <button
            className="md:hidden text-white"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {isOpen && (
          <div className="md:hidden bg-black/95 backdrop-blur-md border-t border-gray-800">
            <div className="px-4 py-4 space-y-3">
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className="block text-gray-300 hover:text-orange-500 transition-colors py-2"
                  onClick={() => setIsOpen(false)}
                >
                  {link.name}
                </a>
              ))}
              <Button className="w-full bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white mt-4">
                Join Now
              </Button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

function Hero() {
  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0">
        <img 
          src="/hero-gym.jpg" 
          alt="Modern Gym" 
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-black/90 via-black/70 to-black/50" />
      </div>
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32">
        <div className="max-w-3xl">
          <Badge className="mb-6 bg-orange-500/20 text-orange-400 border-orange-500/30 hover:bg-orange-500/30">
            <Flame className="w-4 h-4 mr-1" />
            #1 Fitness Center in Bangalore
          </Badge>
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Transform Your Body,{' '}
            <span className="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
              Elevate Your Life
            </span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 leading-relaxed">
            Join Bangalore's premier fitness destination. Experience world-class training, 
            personalized nutrition plans, and a supportive community dedicated to your success.
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <Button size="lg" className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white text-lg px-8">
              Start Your Journey
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
            <Button size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10 text-lg px-8">
              View Programs
            </Button>
          </div>
          
          <div className="mt-12 grid grid-cols-3 gap-8">
            <div>
              <p className="text-4xl font-bold text-orange-500">5000+</p>
              <p className="text-gray-400">Active Members</p>
            </div>
            <div>
              <p className="text-4xl font-bold text-orange-500">50+</p>
              <p className="text-gray-400">Expert Trainers</p>
            </div>
            <div>
              <p className="text-4xl font-bold text-orange-500">24/7</p>
              <p className="text-gray-400">Gym Access</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function About() {
  return (
    <section id="about" className="py-24 bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <Badge className="mb-4 bg-orange-500/20 text-orange-400 border-orange-500/30">
              About Us
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Building a Healthier{' '}
              <span className="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
                Bangalore
              </span>
            </h2>
            <p className="text-gray-400 text-lg mb-6 leading-relaxed">
              Founded in 2015, The Fitness Revolution has grown from a small local gym to Bangalore's 
              most trusted fitness destination. Our mission is to empower individuals to achieve their 
              health goals through expert guidance, cutting-edge facilities, and unwavering support.
            </p>
            <p className="text-gray-400 text-lg mb-8 leading-relaxed">
              We believe fitness is not just about physical strength—it's about mental resilience, 
              nutritional balance, and community connection. Our holistic approach ensures lasting 
              transformations that go beyond the gym.
            </p>
            
            <div className="grid grid-cols-2 gap-6">
              <div className="flex items-start space-x-3">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Dumbbell className="w-6 h-6 text-orange-500" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">Expert Training</h4>
                  <p className="text-gray-400 text-sm">Certified professionals</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Heart className="w-6 h-6 text-orange-500" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">Holistic Wellness</h4>
                  <p className="text-gray-400 text-sm">Mind & body balance</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Zap className="w-6 h-6 text-orange-500" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">Modern Equipment</h4>
                  <p className="text-gray-400 text-sm">State-of-the-art facilities</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Users className="w-6 h-6 text-orange-500" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">Community</h4>
                  <p className="text-gray-400 text-sm">Supportive environment</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="relative">
            <img 
              src="/about-facility.jpg" 
              alt="Gym Facility" 
              className="rounded-2xl shadow-2xl"
            />
            <div className="absolute -bottom-8 -left-8 bg-gradient-to-br from-orange-500 to-red-600 rounded-2xl p-6 shadow-xl">
              <p className="text-4xl font-bold text-white">9+</p>
              <p className="text-white/80">Years of Excellence</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Programs() {
  return (
    <section id="programs" className="py-24 bg-gradient-to-b from-black to-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-orange-500/20 text-orange-400 border-orange-500/30">
            Our Programs
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Choose Your{' '}
            <span className="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
              Fitness Path
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            From high-intensity workouts to mindful yoga sessions, we offer programs designed 
            for every fitness level and goal.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {programs.map((program) => (
            <Card key={program.id} className="bg-gray-900/50 border-gray-800 overflow-hidden group hover:border-orange-500/50 transition-all">
              <div className="relative h-64 overflow-hidden">
                <img 
                  src={program.image} 
                  alt={program.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-gray-900 to-transparent" />
                <div className="absolute bottom-4 left-4 right-4">
                  <h3 className="text-2xl font-bold text-white mb-2">{program.title}</h3>
                  <div className="flex gap-2">
                    <Badge variant="secondary" className="bg-black/50">
                      <Clock className="w-3 h-3 mr-1" />
                      {program.duration}
                    </Badge>
                    <Badge variant="secondary" className="bg-black/50">
                      <Flame className="w-3 h-3 mr-1" />
                      {program.calories} cal
                    </Badge>
                  </div>
                </div>
              </div>
              <CardContent className="p-6">
                <p className="text-gray-400 mb-4">{program.description}</p>
                <div className="flex items-center justify-between">
                  <Badge className="bg-orange-500/20 text-orange-400 border-orange-500/30">
                    {program.level}
                  </Badge>
                  <Button variant="ghost" className="text-orange-500 hover:text-orange-400 hover:bg-orange-500/10">
                    Learn More <ChevronRight className="w-4 h-4 ml-1" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

function Memberships() {
  const [isYearly, setIsYearly] = useState(false);

  return (
    <section id="membership" className="py-24 bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-orange-500/20 text-orange-400 border-orange-500/30">
            Membership Plans
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Invest in Your{' '}
            <span className="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
              Health
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto mb-8">
            Choose a plan that fits your lifestyle. All memberships include access to our 
            state-of-the-art facilities and expert support.
          </p>
          
          <div className="flex items-center justify-center gap-4">
            <span className={`text-sm ${!isYearly ? 'text-white' : 'text-gray-500'}`}>Monthly</span>
            <Switch
              checked={isYearly}
              onCheckedChange={setIsYearly}
            />
            <span className={`text-sm ${isYearly ? 'text-white' : 'text-gray-500'}`}>
              Yearly <span className="text-orange-500">(Save 20%)</span>
            </span>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {memberships.map((plan) => (
            <Card 
              key={plan.id} 
              className={`relative bg-gray-900/50 border-gray-800 ${plan.popular ? 'border-orange-500/50 scale-105' : ''}`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <Badge className="bg-gradient-to-r from-orange-500 to-red-600 text-white">
                    Most Popular
                  </Badge>
                </div>
              )}
              <CardHeader className="p-6">
                <CardTitle className="text-2xl font-bold text-white">{plan.name}</CardTitle>
                <CardDescription className="text-gray-400">{plan.description}</CardDescription>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-white">
                    ₹{isYearly ? plan.priceYearly.toLocaleString() : plan.priceMonthly.toLocaleString()}
                  </span>
                  <span className="text-gray-500">/{isYearly ? 'year' : 'month'}</span>
                </div>
              </CardHeader>
              <CardContent className="p-6 pt-0">
                <ul className="space-y-3">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center text-gray-300">
                      <Check className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                  {plan.notIncluded.map((feature, idx) => (
                    <li key={idx} className="flex items-center text-gray-600">
                      <span className="w-5 h-5 mr-3 flex-shrink-0 text-center">-</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </CardContent>
              <CardFooter className="p-6 pt-0">
                <Button 
                  className={`w-full ${plan.popular 
                    ? 'bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white' 
                    : 'bg-gray-800 hover:bg-gray-700 text-white'}`}
                >
                  Get Started
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

function Trainers() {
  return (
    <section id="trainers" className="py-24 bg-gradient-to-b from-gray-900 to-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-orange-500/20 text-orange-400 border-orange-500/30">
            Expert Trainers
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Meet Your{' '}
            <span className="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
              Fitness Guides
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Our certified trainers bring years of experience and passion to help you achieve your goals.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {trainers.map((trainer) => (
            <Card key={trainer.id} className="bg-gray-900/50 border-gray-800 overflow-hidden group">
              <div className="relative h-80 overflow-hidden">
                <img 
                  src={trainer.image} 
                  alt={trainer.name}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent" />
              </div>
              <CardContent className="p-6">
                <h3 className="text-xl font-bold text-white mb-1">{trainer.name}</h3>
                <p className="text-orange-500 text-sm mb-3">{trainer.role}</p>
                <div className="flex items-center text-gray-400 text-sm mb-3">
                  <Award className="w-4 h-4 mr-1" />
                  {trainer.experience}
                </div>
                <div className="flex flex-wrap gap-2">
                  {trainer.specialization.map((spec, idx) => (
                    <Badge key={idx} variant="secondary" className="bg-gray-800 text-gray-300">
                      {spec}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

function MealPlansSection() {
  const [selectedPlan, setSelectedPlan] = useState<MealPlan | null>(null);

  return (
    <section id="meal-plans" className="py-24 bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-orange-500/20 text-orange-400 border-orange-500/30">
            <Utensils className="w-4 h-4 mr-1" />
            Nutrition Plans
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Fuel Your{' '}
            <span className="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
              Transformation
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Personalized meal plans designed by nutrition experts to complement your fitness journey.
          </p>
        </div>

        <Tabs defaultValue="weight_loss" className="w-full">
          <TabsList className="grid w-full max-w-md mx-auto grid-cols-3 mb-12">
            <TabsTrigger value="weight_loss">Weight Loss</TabsTrigger>
            <TabsTrigger value="muscle_gain">Muscle Gain</TabsTrigger>
            <TabsTrigger value="vegetarian">Vegetarian</TabsTrigger>
          </TabsList>
          
          {mealPlans.map((plan) => (
            <TabsContent key={plan.id} value={plan.category}>
              <Card className="bg-gray-900/50 border-gray-800 overflow-hidden">
                <div className="grid lg:grid-cols-2">
                  <div className="relative h-64 lg:h-auto">
                    <img 
                      src={plan.image} 
                      alt={plan.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="p-8">
                    <h3 className="text-3xl font-bold text-white mb-4">{plan.title}</h3>
                    <p className="text-gray-400 mb-6">{plan.description}</p>
                    
                    <div className="grid grid-cols-4 gap-4 mb-6">
                      <div className="bg-gray-800 rounded-lg p-4 text-center">
                        <p className="text-2xl font-bold text-orange-500">{plan.calories}</p>
                        <p className="text-xs text-gray-400">Calories</p>
                      </div>
                      <div className="bg-gray-800 rounded-lg p-4 text-center">
                        <p className="text-2xl font-bold text-blue-500">{plan.protein}%</p>
                        <p className="text-xs text-gray-400">Protein</p>
                      </div>
                      <div className="bg-gray-800 rounded-lg p-4 text-center">
                        <p className="text-2xl font-bold text-yellow-500">{plan.carbs}%</p>
                        <p className="text-xs text-gray-400">Carbs</p>
                      </div>
                      <div className="bg-gray-800 rounded-lg p-4 text-center">
                        <p className="text-2xl font-bold text-green-500">{plan.fat}%</p>
                        <p className="text-xs text-gray-400">Fat</p>
                      </div>
                    </div>

                    <div className="space-y-3 mb-6">
                      <h4 className="text-white font-semibold flex items-center">
                        <Calendar className="w-5 h-5 mr-2 text-orange-500" />
                        Sample Meals
                      </h4>
                      {plan.meals.slice(0, 3).map((meal, idx) => (
                        <div key={idx} className="flex items-center justify-between bg-gray-800/50 rounded-lg p-3">
                          <div>
                            <p className="text-white font-medium">{meal.name}</p>
                            <p className="text-gray-400 text-sm">{meal.description}</p>
                          </div>
                          <Badge variant="secondary" className="bg-gray-700">
                            {meal.calories} cal
                          </Badge>
                        </div>
                      ))}
                    </div>

                    <Button 
                      className="w-full bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white"
                      onClick={() => setSelectedPlan(plan)}
                    >
                      View Full Plan
                    </Button>
                  </div>
                </div>
              </Card>
            </TabsContent>
          ))}
        </Tabs>

        <Dialog open={!!selectedPlan} onOpenChange={() => setSelectedPlan(null)}>
          <DialogContent className="max-w-2xl bg-gray-900 border-gray-800 text-white">
            <DialogHeader>
              <DialogTitle className="text-2xl">{selectedPlan?.title}</DialogTitle>
              <DialogDescription className="text-gray-400">
                {selectedPlan?.description}
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 mt-4">
              {selectedPlan?.meals.map((meal, idx) => (
                <div key={idx} className="bg-gray-800 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-white">{meal.name}</h4>
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary" className="bg-gray-700">{meal.time}</Badge>
                      <Badge className="bg-orange-500/20 text-orange-400">{meal.calories} cal</Badge>
                    </div>
                  </div>
                  <p className="text-gray-400">{meal.description}</p>
                </div>
              ))}
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </section>
  );
}

function TestimonialsSection() {
  return (
    <section className="py-24 bg-gradient-to-b from-black to-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-orange-500/20 text-orange-400 border-orange-500/30">
            <Star className="w-4 h-4 mr-1" />
            Success Stories
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            What Our{' '}
            <span className="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
              Members Say
            </span>
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial) => (
            <Card key={testimonial.id} className="bg-gray-900/50 border-gray-800">
              <CardContent className="p-6">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                  ))}
                </div>
                <p className="text-gray-300 mb-6 italic">"{testimonial.content}"</p>
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center text-white font-bold">
                    {testimonial.name.charAt(0)}
                  </div>
                  <div className="ml-4">
                    <p className="text-white font-semibold">{testimonial.name}</p>
                    <p className="text-gray-400 text-sm">{testimonial.role}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success('Message sent successfully! We will get back to you soon.');
    setFormData({ name: '', email: '', phone: '', message: '' });
  };

  return (
    <section id="contact" className="py-24 bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-orange-500/20 text-orange-400 border-orange-500/30">
            Get In Touch
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Start Your{' '}
            <span className="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
              Journey Today
            </span>
          </h2>
        </div>

        <div className="grid lg:grid-cols-2 gap-16">
          <div>
            <h3 className="text-2xl font-bold text-white mb-6">Contact Information</h3>
            <div className="space-y-6 mb-8">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <MapPin className="w-6 h-6 text-orange-500" />
                </div>
                <div>
                  <h4 className="text-white font-semibold mb-1">Location</h4>
                  <p className="text-gray-400">123 Fitness Avenue, Koramangala<br />Bangalore, Karnataka 560034</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Phone className="w-6 h-6 text-orange-500" />
                </div>
                <div>
                  <h4 className="text-white font-semibold mb-1">Phone</h4>
                  <p className="text-gray-400">+91 80 1234 5678</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Mail className="w-6 h-6 text-orange-500" />
                </div>
                <div>
                  <h4 className="text-white font-semibold mb-1">Email</h4>
                  <p className="text-gray-400">info@fitnessrevolution.in</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Clock className="w-6 h-6 text-orange-500" />
                </div>
                <div>
                  <h4 className="text-white font-semibold mb-1">Working Hours</h4>
                  <p className="text-gray-400">Monday - Friday: 5:00 AM - 11:00 PM<br />
                  Saturday - Sunday: 6:00 AM - 10:00 PM</p>
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Follow Us</h4>
              <div className="flex space-x-4">
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:bg-orange-500 hover:text-white transition-colors">
                  <Instagram className="w-5 h-5" />
                </a>
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:bg-orange-500 hover:text-white transition-colors">
                  <Facebook className="w-5 h-5" />
                </a>
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:bg-orange-500 hover:text-white transition-colors">
                  <Twitter className="w-5 h-5" />
                </a>
              </div>
            </div>
          </div>

          <Card className="bg-gray-900/50 border-gray-800">
            <CardHeader>
              <CardTitle className="text-white">Send us a Message</CardTitle>
              <CardDescription className="text-gray-400">
                Fill out the form below and we'll get back to you as soon as possible.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="name" className="text-gray-300">Full Name</Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="bg-gray-800 border-gray-700 text-white"
                    placeholder="Your name"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="email" className="text-gray-300">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="bg-gray-800 border-gray-700 text-white"
                    placeholder="your@email.com"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="phone" className="text-gray-300">Phone</Label>
                  <Input
                    id="phone"
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="bg-gray-800 border-gray-700 text-white"
                    placeholder="+91 98765 43210"
                  />
                </div>
                <div>
                  <Label htmlFor="message" className="text-gray-300">Message</Label>
                  <Textarea
                    id="message"
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    className="bg-gray-800 border-gray-700 text-white"
                    placeholder="How can we help you?"
                    rows={4}
                    required
                  />
                </div>
                <Button 
                  type="submit"
                  className="w-full bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white"
                >
                  Send Message
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="bg-gray-900 border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-4 gap-12">
          <div className="col-span-2">
            <div className="flex items-center space-x-2 mb-6">
              <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center">
                <Dumbbell className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Fitness Revolution</span>
            </div>
            <p className="text-gray-400 mb-6 max-w-md">
              Transforming lives through fitness, nutrition, and community. Join Bangalore's 
              premier fitness destination and start your journey to a healthier you.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-orange-500 transition-colors">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-orange-500 transition-colors">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-orange-500 transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
            </div>
          </div>
          
          <div>
            <h4 className="text-white font-semibold mb-6">Quick Links</h4>
            <ul className="space-y-3">
              <li><a href="#home" className="text-gray-400 hover:text-orange-500 transition-colors">Home</a></li>
              <li><a href="#about" className="text-gray-400 hover:text-orange-500 transition-colors">About Us</a></li>
              <li><a href="#programs" className="text-gray-400 hover:text-orange-500 transition-colors">Programs</a></li>
              <li><a href="#membership" className="text-gray-400 hover:text-orange-500 transition-colors">Membership</a></li>
              <li><a href="#trainers" className="text-gray-400 hover:text-orange-500 transition-colors">Trainers</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-white font-semibold mb-6">Support</h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-gray-400 hover:text-orange-500 transition-colors">FAQ</a></li>
              <li><a href="#" className="text-gray-400 hover:text-orange-500 transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="text-gray-400 hover:text-orange-500 transition-colors">Terms of Service</a></li>
              <li><a href="#contact" className="text-gray-400 hover:text-orange-500 transition-colors">Contact Us</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-12 pt-8 text-center">
          <p className="text-gray-500">
            © 2024 The Fitness Revolution. All rights reserved. Made with passion in Bangalore.
          </p>
        </div>
      </div>
    </footer>
  );
}

// Main App
function App() {
  return (
    <div className="min-h-screen bg-black">
      <Navbar />
      <main>
        <Hero />
        <About />
        <Programs />
        <Memberships />
        <Trainers />
        <MealPlansSection />
        <TestimonialsSection />
        <Contact />
      </main>
      <Footer />
    </div>
  );
}

export default App;
