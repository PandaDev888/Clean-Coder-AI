import { useState } from "react";

interface ProfileCardProps {
  item: {
    uuid: string;
    full_name: string;
    short_bio?: string;
    bio?: string;
  };
  onConnect: (uuid: string) => void; // used in New tab
  onAccept: (invitationId: string) => void; // used in Received tab
  onReject: (invitationId: string) => void; // used in Received tab
  onCancel: (invitationId: string) => void;  // used in Sent tab
  activeTab?: "New" | "Received" | "Sent";
}

export default function ProfileCard({ item, onConnect, onAccept, onReject, onCancel, activeTab }: ProfileCardProps) {
  const [loading, setLoading] = useState(false);

  const handleAction = async (action: () => Promise<void>) => {
    setLoading(true);
    try {
      await action();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="bg-white rounded-lg p-4 border-b cursor-pointer"
    >
      <h2 className="text-lg font-medium mb-2">
        {item.full_name}
      </h2>
      
      {item.short_bio && (
        <p className="text-gray-600 mb-2">{item.short_bio}</p>
      )}
      {item.bio && (
        <p className="text-gray-600 mb-4">{item.bio}</p>
      )}
      
      {activeTab === "New" && (
        <button
          onClick={(e) => {
            e.stopPropagation(); // Prevent card click event
            onConnect(item.uuid);
          }}
          className="text-blue-600 font-medium"
        >
          + Connect
        </button>
      )}
      {activeTab === "Received" && (
        <div className="flex gap-4">
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleAction(() => onAccept(item.uuid));
            }}
            className="text-blue-600"
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Accept'}
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleAction(() => onReject(item.uuid));
            }}
            className="text-red-600"
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Reject'}
          </button>
        </div>
      )}
      {activeTab === "Sent" && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleAction(() => onCancel(item.uuid));
          }}
          className="text-gray-600"
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Cancel'}
        </button>
      )}
    </div>
  );
}