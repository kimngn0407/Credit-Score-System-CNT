package com.example.LoanSystem.Services;

import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

@Service
@Slf4j
public class CurrencyConverterService {
    
    // Tỷ giá VND/USD (có thể cấu hình từ environment)
    private static final double VND_TO_USD_RATE = 1.0 / 24000.0; // 1 VND = 1/24000 USD
    private static final double USD_TO_VND_RATE = 24000.0; // 1 USD = 24000 VND
    
    /**
     * Chuyển đổi từ VND sang USD cho model
     */
    public double convertVndToUsd(double vndAmount) {
        double usdAmount = vndAmount * VND_TO_USD_RATE;
        log.debug("Converting {} VND to {} USD", vndAmount, usdAmount);
        return usdAmount;
    }
    
    /**
     * Chuyển đổi từ USD sang VND cho frontend
     */
    public double convertUsdToVnd(double usdAmount) {
        double vndAmount = usdAmount * USD_TO_VND_RATE;
        log.debug("Converting {} USD to {} VND", usdAmount, vndAmount);
        return vndAmount;
    }
    
    /**
     * Chuyển đổi person_income từ VND sang USD
     */
    public double convertIncomeVndToUsd(double incomeVnd) {
        return convertVndToUsd(incomeVnd);
    }
    
    /**
     * Chuyển đổi loan_amnt từ VND sang USD
     */
    public double convertLoanAmountVndToUsd(double loanAmountVnd) {
        return convertVndToUsd(loanAmountVnd);
    }
    
    /**
     * Chuyển đổi person_income từ USD sang VND
     */
    public double convertIncomeUsdToVnd(double incomeUsd) {
        return convertUsdToVnd(incomeUsd);
    }
    
    /**
     * Chuyển đổi loan_amnt từ USD sang VND
     */
    public double convertLoanAmountUsdToVnd(double loanAmountUsd) {
        return convertUsdToVnd(loanAmountUsd);
    }
    
    /**
     * Lấy tỷ giá hiện tại
     */
    public double getVndToUsdRate() {
        return VND_TO_USD_RATE;
    }
    
    /**
     * Lấy tỷ giá ngược
     */
    public double getUsdToVndRate() {
        return USD_TO_VND_RATE;
    }
}
