"use client";

import { useState, useEffect } from "react";
import { UserIcon, AcademicCapIcon, ClockIcon, TrophyIcon } from "@heroicons/react/24/outline";
import { PR0101001, PR0101001Response } from "@/services/PR0101Service";

export default function ProfilePage() {
  const [profile, setProfile] = useState<PR0101001Response | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setLoading(true);

        // プロフィール情報のみ取得（API ID: PR0101001）
        const profileData = await PR0101001();
        setProfile(profileData);
      } catch (err) {
        console.error("プロフィールデータ取得エラー:", err);
        setError("プロフィール情報の取得に失敗しました");
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, []);

  // 日付フォーマット関数
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("ja-JP", {
      year: "numeric",
      month: "long",
    });
  };

  if (loading) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
          <div className="space-y-6">
            <div className="h-32 bg-gray-200 rounded"></div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="h-24 bg-gray-200 rounded"></div>
              <div className="h-24 bg-gray-200 rounded"></div>
              <div className="h-24 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">エラー</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!profile) {
    return null;
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">プロフィール</h1>
        <p className="text-gray-600">あなたの学習進捗と実績を確認できます。</p>
      </div>

      {/* ユーザー情報 */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center mb-4">
          <div className="bg-gray-200 rounded-full p-3 mr-4">
            <UserIcon className="h-12 w-12 text-gray-600" />
          </div>
          <div>
            <h2 className="text-2xl font-semibold text-gray-900">{profile.username}</h2>
            <p className="text-gray-600">{profile.email}</p>
            <p className="text-sm text-gray-500">参加日: {formatDate(profile.created_at)}</p>
          </div>
        </div>
      </div>

      {/* 学習統計 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <AcademicCapIcon className="h-8 w-8 text-blue-600 mr-3" />
            <div>
              <p className="text-2xl font-bold text-gray-900">-</p>
              <p className="text-gray-600">完了演習</p>
              <p className="text-sm text-gray-500">準備中</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <ClockIcon className="h-8 w-8 text-green-600 mr-3" />
            <div>
              <p className="text-2xl font-bold text-gray-900">-</p>
              <p className="text-gray-600">学習時間</p>
              <p className="text-sm text-gray-500">準備中</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <TrophyIcon className="h-8 w-8 text-yellow-600 mr-3" />
            <div>
              <p className="text-2xl font-bold text-gray-900">-</p>
              <p className="text-gray-600">総スコア</p>
              <p className="text-sm text-gray-500">準備中</p>
            </div>
          </div>
        </div>
      </div>

      {/* 今後の機能予定エリア */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">今後の機能</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
            <div className="flex items-center mb-2">
              <TrophyIcon className="h-5 w-5 text-gray-400 mr-2" />
              <h4 className="font-medium text-gray-500">実績システム</h4>
            </div>
            <p className="text-sm text-gray-400">学習の成果に応じてバッジを獲得できる機能を準備中です。</p>
          </div>

          <div className="p-4 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
            <div className="flex items-center mb-2">
              <ClockIcon className="h-5 w-5 text-gray-400 mr-2" />
              <h4 className="font-medium text-gray-500">学習ストリーク</h4>
            </div>
            <p className="text-sm text-gray-400">連続学習日数を追跡する機能を準備中です。</p>
          </div>
        </div>
      </div>
    </div>
  );
}
