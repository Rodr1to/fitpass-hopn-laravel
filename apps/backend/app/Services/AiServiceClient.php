<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class AiServiceClient
{
    protected string $recommenderUrl;
    protected string $anomalyUrl;
    protected string $routerUrl;

    public function __construct()
    {
        $this->recommenderUrl = config('services.ai.recommender_url');
        $this->anomalyUrl = config('services.ai.anomaly_url');
        $this->routerUrl = config('services.ai.router_url');
    }

    /**
     * Get a plan recommendation from the AI service.
     */
    public function getPlanRecommendation(array $userProfile): ?string
    {
        $response = Http::timeout(5)->post($this->recommenderUrl . '/recommend', $userProfile);

        if ($response->successful()) {
            return $response->json('recommended_plan');
        }

        Log::error('AI Recommender service failed.', [
            'status' => $response->status(), 
            'body' => $response->body()
        ]);
        
        return null; // Return null on failure
    }

    /**
     * Get a list of check-in anomalies from the AI service.
     */
    public function getCheckinAnomalies(array $checkins): ?array
    {
        $payload = ['checkins' => $checkins];
        $response = Http::timeout(15)->post($this->anomalyUrl . '/detect', $payload);

        if ($response->successful()) {
            return $response->json('anomalies');
        }

        Log::error('AI Anomaly service failed.', [
            'status' => $response->status(), 
            'body' => $response->body()
        ]);
        
        return null;
    }

    /**
     * Get a language routing suggestion from the AI service.
     */
    public function getLanguageRoute(string $text): ?array
    {
        $payload = ['text' => $text];
        $response = Http::timeout(3)->post($this->routerUrl . '/route', $payload);

        if ($response->successful()) {
            return $response->json();
        }

        Log::error('AI Router service failed.', [
            'status' => $response->status(), 
            'body' => $response->body()
        ]);
        
        return null;
    }
}
