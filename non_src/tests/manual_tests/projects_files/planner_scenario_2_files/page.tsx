"use client";

import {{ useState, useEffect }} from "react";
import Image from "next/image";
import {{ useRouter }} from "next/navigation";
import ProfileCard from "./components/ProfileCard";
import PopupNotification from "./components/PopupNotification";

interface ProfileItem {{
  uuid: string;
  full_name: string;
  short_bio?: string;
  bio?: string;
}}

export default function Home() {{
  const [activeTab, setActiveTab] = useState<'New' | 'Received' | 'Sent'>('New');
  const [NewItems, setNewItems] = useState<ProfileItem[]>([]);
  const [receivedItems, setReceivedItems] = useState<ProfileItem[]>([]);
  const [sentItems, setSentItems] = useState<ProfileItem[]>([]);
  const [error, setError] = useState('');
  const [notification, setNotification] = useState<{{ message: string, type: 'positive' | 'negative' }} | null>(null);
  const [loading, setLoading] = useState(false);
  const [iconLoading, setIconLoading] = useState(true);
  const router = useRouter();


  async function handleConnect(uuid: string) {{
    setLoading(true);
    try {{
      const token = localStorage.getItem('token');
      if (!token) throw new Error('Authentication token not found');
      const response = await fetch(`${{process.env.NEXT_PUBLIC_API_URL}}/invitations/create/${{uuid}}`, {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${{token}}`,
        }},
      }});
      if (!response.ok) throw new Error('Failed to create invitation');
      setNotification({{ message: 'Invitation sent successfully', type: 'positive' }});

      // Optimistically update the New list
      setNewItems((prevItems) => prevItems.filter(item => item.uuid !== uuid));
    }} catch (err: any) {{
      setNotification({{ message: err.message, type: 'negative' }});
    }} finally {{
      setLoading(false);
      setTimeout(() => setNotification(null), 3000);
    }}
  }}

  async function handleAccept(invitationId: string) {{
    setLoading(true);
    try {{
      const token = localStorage.getItem('token');
      if (!token) throw new Error('Authentication token not found');
      const response = await fetch(`${{process.env.NEXT_PUBLIC_API_URL}}/invitations/accept/${{invitationId}}`, {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${{token}}`,
        }},
      }});
      if (!response.ok) throw new Error('Failed to accept invitation');
      setNotification({{ message: 'Invitation accepted successfully', type: 'positive' }});
      setReceivedItems((prevItems) => prevItems.filter(item => item.uuid !== invitationId));
    }} catch (err: any) {{
      setNotification({{ message: err.message, type: 'negative' }});
    }} finally {{
      setLoading(false);
      setTimeout(() => setNotification(null), 3000);
    }}
  }}

  async function handleReject(invitationId: string) {{
    setLoading(true);
    try {{
      const token = localStorage.getItem('token');
      if (!token) throw new Error('Authentication token not found');
      const response = await fetch(`${{process.env.NEXT_PUBLIC_API_URL}}/invitations/reject/${{invitationId}}`, {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${{token}}`,
        }},
      }});
      if (!response.ok) throw new Error('Failed to reject invitation');
      setNotification({{ message: 'Invitation rejected successfully', type: 'positive' }});
      setReceivedItems((prevItems) => prevItems.filter(item => item.uuid !== invitationId));
    }} catch (err: any) {{
      setNotification({{ message: err.message, type: 'negative' }});
    }} finally {{
      setLoading(false);
      setTimeout(() => setNotification(null), 3000);
    }}
  }}

  async function handleCancel(invitationId: string) {{
    setLoading(true);
    try {{
      const token = localStorage.getItem('token');
      if (!token) throw new Error('Authentication token not found');
      const response = await fetch(`${{process.env.NEXT_PUBLIC_API_URL}}/invitations/cancel/${{invitationId}}`, {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${{token}}`,
        }},
      }});
      if (!response.ok) throw new Error('Failed to cancel invitation');
      setNotification({{ message: 'Invitation canceled successfully', type: 'positive' }});
      setSentItems((prevItems) => prevItems.filter(item => item.uuid !== invitationId));
    }} catch (err: any) {{
      setNotification({{ message: err.message, type: 'negative' }});
    }} finally {{
      setLoading(false);
      setTimeout(() => setNotification(null), 3000);
    }}
  }}
  async function fetchNew() {{
    try {{
      const userRole = localStorage.getItem('role');
      const token = localStorage.getItem('token');
      
      if (!token) {{
        throw new Error('Authentication token not found');
      }}

      if (!userRole) {{
        throw new Error('User role not found');
      }}

      const url = `${{process.env.NEXT_PUBLIC_API_URL}}${{
        userRole === "intern"
          ? '/fetch-campaigns-for-main-page'
          : '/fetch-interns-for-main-page'
      }}`;

      console.log('Fetching from URL:', url); // Debug log
      
      const response = await fetch(url, {{
        method: 'GET',
        headers: {{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${{token}}`,
        }},
      }});

      if (!response.ok) {{
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch New items');
      }}

      const data = await response.json();
      setNewItems(data.items || []);
    }} catch (err: any) {{
      console.error('Fetch error:', err); // Debug log
      setError(err.message);
      setTimeout(() => setError(''), 3000);
    }}
  }}

  async function fetchReceived() {{
    try {{
      const token = localStorage.getItem('token');
      const response = await fetch(`${{process.env.NEXT_PUBLIC_API_URL}}/invitations/received`, {{
        method: 'GET',
        headers: {{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${{token}}`,
        }},
      }});
      if (!response.ok) throw new Error('Failed to fetch received invitations');
      const data = await response.json();
      setReceivedItems(data.items || []);
    }} catch (err: any) {{
      setError(err.message);
      setTimeout(() => setError(''), 3000);
    }}
  }}

  async function fetchSent() {{
    try {{
      const token = localStorage.getItem('token');
      const response = await fetch(`${{process.env.NEXT_PUBLIC_API_URL}}/invitations/sent`, {{
        method: 'GET',
        headers: {{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${{token}}`,
        }},
      }});
      if (!response.ok) throw new Error('Failed to fetch sent invitations');
      const data = await response.json();
      setSentItems(data.items || []);
    }} catch (err: any) {{
      setError(err.message);
      setTimeout(() => setError(''), 3000);
    }}
  }}

  useEffect(() => {{
    const token = localStorage.getItem('token');
    if (!token) {{
      setError('Please login first');
      return;
    }}
    fetchNew();
  }}, []);

  const handleTabClick = (tab: 'New' | 'Received' | 'Sent') => {{
    setActiveTab(tab);
    if (tab === 'New') fetchNew();
    if (tab === 'Received') fetchReceived();
    if (tab === 'Sent') fetchSent();
  }};

  let listToRender: ProfileItem[] = [];
  if (activeTab === 'New') listToRender = NewItems;
  if (activeTab === 'Received') listToRender = receivedItems;
  if (activeTab === 'Sent') listToRender = sentItems;

  return (
    <main className="max-w-2xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
      <header className="flex items-center justify-between mb-8">
          <button className="w-10 h-10 rounded-full bg-[#EEEEEE] flex items-center justify-center">
            <Image 
              src="/profile.svg" 
              alt="Profile" 
              width={{24}} 
              height={{24}} 
              onError={{(e) => e.currentTarget.src = '/fallback-icon.svg'}} // Fallback icon
            />
          </button>
        <h1 className="text-xl font-semibold">my app</h1>
        <button className="w-10 h-10 rounded-full bg-[#EEEEEE] flex items-center justify-center">
          <Image src="/icons/search.svg" alt="Search" width={{24}} height={{24}} />
        </button>
      </header>

      <nav className="flex p-1 mb-8 justify-center bg-[#F5F5F5]/40 rounded-full max-w-md mx-auto">
        {{["New", "Received", "Sent"].map((tab) => (
          <button
            key={{tab}}
            onClick={{() => handleTabClick(tab as 'New' | 'Received' | 'Sent')}}
            className={{`flex-1 px-6 py-2.5 rounded-full text-sm transition-all duration-300 ${{
              activeTab === tab
                ? "bg-white font-medium text-black shadow-sm text-[15px]"
                : "text-gray-400/80 hover:text-gray-500"
            }}`}}
          >
            {{tab}}
          </button>
        ))}}
      </nav>

      {{error && (
        <div className="mb-6 py-2 px-4 w-full text-center bg-[#FFF2F2] text-[#FF0000] text-[14px] rounded-full">
          {{error}}
        </div>
      )}}

      <section className="space-y-4">
        {{listToRender.length === 0 ? (
          <div className="text-center py-4 text-gray-500">No items found</div>
        ) : (
          listToRender.map((item) => (
            <ProfileCard
              key={{item.uuid}}
              item={{item}}
              onConnect={{handleConnect}}
              onAccept={{handleAccept}}
              onReject={{handleReject}}
              onCancel={{handleCancel}}
              activeTab={{activeTab}}
            />
          ))
        )}}
      </section>

      {{notification && (
        <PopupNotification
          message={{notification.message}}
          type={{notification.type}}
          onClose={{() => setNotification(null)}}
        />
      )}}
    </main>
  );
}}