      PROGRAM INT6_271M

C     corrected calculation of optical depth from DFDC
C     int6_271 provides for a solar zenith angle which varies with layer
C     The file THETAS_LAYERS.DAT must contain a solar zenith angle for
C     for each layer in the model.
C     MODIFIED FOR 30 LAYERS AND 31 LEVELS - 7/2/91 AME 
C     MODIFIED TO RUN SUN-STANDARD DOUBLE PRECISION ON A
C     SUN (OR COMPATIBLE) MINICOMPUTER. 2/26/91 - AME
C     VERSION MODIFIED FOR PERKIN-ELMER 3240 ON 4/23/87
C     COMPUTES INTENSITIES FOR INHOMOGENEOUS CLOUD LAYERS
C         - LRD
C     INTENSI3.FTN allows the zenith angle of the Sun to vary with
C     level.  4/19/88 - LRD
C     Changed back to ability to read in THETAS from a file.
C     1/19/90 - LRD
C     INTENSI4.FTN is modified to do single scattering analytically.
C     This mean you can get away with using only 6 - 8 Fourier
C     coefficients.
C     UPDATED TO HANDLE 32 FOURIER COEFFICIENTS - 8/14/97 - LRD
C     UPDATED TO RUN VARIABLE (NUMG) NUMBER OF GAUSS QUADRATURE POINTS
C     PROGRAM MUST BE RECOMPILED IF NUMBER OF GAUSS POINTS IS CHANGED
C     ALSO CHANGED GRID OF AZIMUTH ANGLES AT ERIC WEGRYN'S REQUEST
C     11/20/97 - LRD
C     Adapted for HP 9000/735.  Compile with
C       f77 -g +e -V +R -R8 +autodblpad -o int6_271m int6_271m.f for debugging
C       f77 -O +e -K -R8 +autodblpad -o int6_271m int6_271m.f for optimization
C       - 4/7/97 - LRD
C
C     for Fortran 90 use:
C       f90 -g +r8 +save -o int6_271 int6_271.f for debugging
C       f90 -O +r8 +save -o int6_271 int6_271.f for optimization
C
C     for Fortran 77 (Portland Group compiler) use
C       f77 -g -r8 -Msave -Mlfs -o int6_271m int6_271m.f for debugging
C       f77 -fast -r8 -Msave -Mlfs -o int6_271m int6_271m.f for optimization
C
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
C                                                                    C
C                                                                    C
C                                 M O D E L                          C
C                                                                    C
C                                                                    C
C             I I I I I TAUA(1)---------------------- LEV = 1        C
C             I I I I V       LAYER 1  TAU(1)  W(1)                  C
C             I I I I TAUA(2)------------------------ LEV = 2        C
C             I I I V         LAYER 2  TAU(2)  W(2)                  C
C             I I I TAUA(3)-------------------------- LEV = 3        C
C             I I I                  .                               C
C             I I I                  .                               C
C             I I V                  .                               C
C             I I TAUA(NLAY-1)----------------------- LEV = NLAY-1   C
C             I I                 LAYER(NLAY-1)                      C
C             I V             TAU(NLAY-1)  W(NLAY-1)                 C
C             I TAUA(NLAY)--------------------------- LEV = NLAY     C
C             I                   LAYER(NLAY)                        C
C             V              TAU(NLAY)  W(NLAY)                      C
C             TAUA(NBOT)----------------------------- LEV = NBOT     C
C                        //////// G R O U N D ///////                C
C                                                                    C
C                                                                    C
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

      PARAMETER (LA=31,LE=32,NUMG=64,NAZ=38,NUMCOEFS=256)
      LOGICAL DONE
      CHARACTER datestr*9,timestr*8
      REAL LAMMIN,LAMMAX,MU,MUSUN(LE),THETAS(LE)
      COMMON NUM,NMAX,SCRIT,MU(NUMG),WT(NUMG),HWTOMU(NUMG),QWTOMU(NUMG),
     & M
      COMMON/L/ALF,LAMMIN,LAMMAX,GR,F0,NLAY,MAXM,MLAY
      COMMON /PHASEFN/ P(271,LA),THETAP(271)
      COMMON/HAPKE/HAPKE_B0,HAPKE_B,HAPKE_C,HAPKE_H
      DIMENSION GWAVMIN(200),GWAVMAX(200),GROUND(200)
      DIMENSION SM(NUMCOEFS,NUMG),SSM(NUMCOEFS,NUMG)
      DIMENSION TAUFRACC(LE),TAUAC(LE),DFDC(LE),FDC(LE),FUC(LE),
     & FNETC(LE),WC(LE),TAUC(LE)
      DIMENSION SSO(LE,NUMG,NUMG),STO(LE,NUMG,NUMG),UIS(NUMG,NUMG),
     & UISTEMP(NUMG)
      DIMENSION DISTEMP(NUMG),UISSUN(NUMG),DISSUN(NUMG)
      DIMENSION SSA(NUMG,NUMG),TSA(NUMG,NUMG),SSAO(NUMG,NUMG),
     & TSAO(NUMG,NUMG)
      DIMENSION SSB(NUMG,NUMG),TSB(NUMG,NUMG)
      DIMENSION TAU(LA),W(LA),TAUA(LE),WTMU(NUMG)
      DIMENSION THETA(NUMG)
      DIMENSION UISUN(NUMG),DISUN(NUMG),UITEMP(NUMG),DITEMP(NUMG),
     & MLAY(LA)
      CHARACTER ALF*132
      DIMENSION SO(LE,NUMG,NUMG), SA(NUMG,NUMG),SB(NUMG,NUMG),
     & TA(NUMG,NUMG),TB(NUMG,NUMG)
      DIMENSION DSUM(LE,NAZ,NUMG),USUM(LE,NAZ,NUMG),FOCOS(NAZ,NUMCOEFS)
      DIMENSION DSUMC(LE,NAZ,NUMG),USUMC(LE,NAZ,NUMG)
      DIMENSION DPHID(NAZ),DPHI(NAZ)
      DIMENSION FU(LE),FD(LE),DFD(LE),FNET(LE)
      DIMENSION UI(NUMG,NUMG), DI(NUMG,NUMG),SAI(NUMG,NUMG),
     & SAO(NUMG,NUMG),TAO(NUMG,NUMG)
      DIMENSION ALT(31)
C      DATA ALT/404.0,298.0,208.0,200.0,192.0,184.0,176.0,168.0,160.0,
C     & 152.0,144.0,136.0,128.0,120.0,112.0,104.0, 96.0, 88.0, 80.0, 
C     & 72.0, 64.0, 56.0, 48.0, 42.0, 36.0, 30.0, 24.0, 18.0, 12.0,
C     & 6.0,  0.0/
      DATA ALT/500.0,190.0,144.0,124.0,110.0,100.0,92.0,86.0,80.0,
     & 75.0,70.0,65.0,60.0,55.0,50.0,45.0, 40.0, 35.0, 30.0, 
     & 27.0, 24.0, 21.0, 18.0, 15.0, 12.0, 10.0, 8.0, 6.0, 4.0,
     & 2.0,  0.0/
      EQUIVALENCE (SA(1,1),SAO(1,1)),(TA(1,1),TB(1,1),UI(1,1))
      DATA PI/3.14159265358979/
      DATA DPHID/ 0.,1.,2.,3.,4.,5.,6.,8.,10.,12.,13.,14.,
     1   15.,17.,18.,20.,25.,30.,35.,40.,50.,60.,70.,80.,90.,100.,
     1   110.,120.,130.,140.,150.,155.,160.,165.,170.,175.,178.,180./
C      DATA DPHID/ 0.0,1.0,2.0,3.0,4.0,7.0,10.0,15.0,20.0,30.0,40.0,
C    1   50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,
C    1   155.0,160.0,165.0,170.0,175.0,178.0,180.0/
C     GAUSSIAN POINTS AND WEIGHTS FOR 0 TO 1 QUADRATURE
C     DATA GMU/-0.9782286581461, -0.8870625997681, -0.7301520055740,
C    1-0.5190961292068, -0.2695431559523, 0.0/
C     DATA GW/0.0556685671162, 0.1255803694649, 0.1862902109277,
C    10.2331937645920, 0.2628045445102, 0.2729250867779/
      DATA OLAMMIN/-99.0/
 1000 FORMAT (///,10X,I2,' GAUSSIAN POINTS AND WEIGHTS'///
     1 12X,'I',23X,'MU',23X,'WT',13X,'THETA',19X,'HWTOMU',19X,'QWTOMU'/)
 1001 FORMAT(10X,I3,2(5X,0PE20.13),10X,F8.4,2(5X,E20.13))
C1002 FORMAT (A132)
C1003 FORMAT (//1X,A,//)
C1005 FORMAT (3F10.0,3I5,F10.0,5X,I5)
 1006 FORMAT (' WAVELENGTH = ',F11.7,' MICRONS',
     1 ' GROUND REFLECTIVITY = ',F9.6/
     1 ' NUMBER OF LAYERS = ',I5,/
     1 ' SOLAR ZENITH ANGLE = ',F8.4/
     1 ' EARTH SOLAR FLUX = ',F11.5,'     (WATTS/SQ METER)')
C1007 FORMAT (F10.6,F10.3,I5)
 1008 FORMAT (1X,I5,F15.6,F15.4)
 1009 FORMAT (  ' SPHERICAL ALBEDO =',F9.6,' BETWEEN',F10.7,
     1 ' AND',F10.7,' MICRONS'/)
 1010 FORMAT (//' LEVEL',5X,'  ALT',7X,'TAUA',9X,'DFD',10X,'FD',10X,
     1  'FU',8X,'FNET',32X,'W',7X,'TAU',1X,'UNIT'/)
C1011 FORMAT (' UI ',1P11E11.4/' DI ',1P11E11.4)
C1012 FORMAT (I5,(12F6.0))
C1013 FORMAT (//I10,' NON-STANDARD FLUX POINTS',//(12F10.4))
 1014 FORMAT (1X,I5,F10.3,F11.4,1P4E12.5,24X,0PF9.6,F10.3)
C1015 FORMAT (//5X,'N',3X,'FLUX PT',8X,'TAU',9X,'DFD',10X,'FD',10X,
C    1  'FU',8X,'FNET',6X,'DFDSUM',7X,'FDSUM',7X,'FUSUM',5X,'FNETSUM'/)
C1016 FORMAT (/' LEVEL',I5)

      RADEG=PI/180.0
      DONE=.FALSE.
      OPEN(2,FILE='THETAS_LAYER.DAT',STATUS='OLD')


1301  DO 7 I=1,LE
      READ(2,*,END=4004) THETASD
      THETAS(I)=THETASD
      MUSUN(I)=COS(THETAS(I)*RADEG)
      TAUFRACC(I)=0.
      TAUAC(I)=0.
      DFDC(I)=0.
      FDC(I)=0.
      FUC(I)=0.
      FNETC(I)=0.
      WC(I)=0.
      TAUC(I)=0.
      DO 1370 NA=1,NANG
        DO 1380 L=1,NUM
          USUMC(L,NA,L)=0.
          DSUMC(L,NA,L)=0.
1380    CONTINUE
1370  CONTINUE
7     CONTINUE
C
C     OPEN THE INPUT FILE CONTAINING THE S AND T FUNCTIONS (GENERATED
C     BY INTSCLD.FTN)
C
4004  OPEN(10,FILE='TAPE10I.DAT',STATUS='OLD',
     & FORM='UNFORMATTED',ACCESS='DIRECT',IOSTAT=IOS,
     & RECL=NUMG*NUMG*32+16)
      IF(IOS.NE.0) THEN
         WRITE(6,5001) IOS
5001  format(' ERROR ',I3,' OPENING TAPE10I.DAT')
         STOP
      ENDIF
C
C     ALSO OPEN THE PRINTER OUTPUT FILE (UNIT 6)
C
4002  OPEN(8,IOSTAT=IOS,FILE='INTENSI.OUT',
     &STATUS='UNKNOWN')
      IF(IOS.NE.0) THEN
         WRITE(6,5002) IOS
5002  format(' ERROR ',I3,' OPENING INTENSI.OUT')
         STOP
      ENDIF

C     Write the date and time at the top of the output file
C      call date(datestr)
C      call time(timestr)
      call DATE_AND_TIME(datestr,timestr)
      write(8,1016) datestr,timestr
1016  format(1x,a9,1x,a8)
      
C     Copy the input NAMLIST.INT file to the output file
      OPEN(11,FILE='namlist.int',STATUS='OLD')
      DO I=1,30000
        READ(11,5010,END=1313) ALF
        WRITE(8,5010) ALF
5010    format(A)
      END DO
1313  CLOSE(11)
      
C     Copy the input atmos.new file to the output file
      OPEN(11,FILE='atmos.new',STATUS='OLD')
      DO I=1,10000
        READ(11,5010,END=1314) ALF
        WRITE(8,5010) ALF
      END DO
1314  CLOSE(11)

      CALL RENEW('./INTENSI.ALB')
      OPEN(9,IOSTAT=IOS,FILE='INTENSI.ALB',STATUS='NEW')
      IF(IOS.NE.0) THEN
         WRITE(6,5003) IOS
5003  format(' ERROR ',I3,' OPENING INTENSI.ALB')
         STOP
      ENDIF
      WRITE(9,5004)
5004  format('     MIN     MAX     CTR     SPH    GEOM')

C     Generate scattering angles for phase functions
      DO 123 I=1,271
      THETAP(I)=(MIN(I-1,100)*0.1 + MAX(I-101,0)*1.0)*RADEG
  123 CONTINUE

C     NUM = NUMBER OF GAUSS QUADRATURE POINTS
      NUM = NUMG
      NUMHAF = (NUM+1)/2
C      NMAX = NUMG
      NMAX = 15
C      SCRIT = .003
      SCRIT = .0000003
C     DO 1 I = 1,NUMHAF
C     J = NUM-I+1
C     GMUHAF = 0.5*GMU(I)
C     MU(I) = 0.5 + GMUHAF
C     MU(J) = 0.5 - GMUHAF
C     WT(I) = 0.5*GW(I)
C   1 WT(J) = WT(I)
      CALL GAULEG(0.0,1.0,MU,WT,NUM)
      WRITE(8,1000) NUM
      DO 2 I = 1,NUM
      HWTOMU(I) = 0.5*WT(I)/MU(I)
      QWTOMU(I) = 0.5*HWTOMU(I)
      THETA(I) = ACOS(MU(I))/RADEG
    2 WRITE(8,1001)    I,MU(I),WT(I),THETA(I),HWTOMU(I),QWTOMU(I)

C     SET DESIRED AZIMUTH ANGLES
      NANG = NAZ
      DPHI(1) = 0
      DO 4 NA = 2,NANG
    4 DPHI(NA) = RADEG*DPHID(NA)

C     READ DATA FOR THIS WAVELENGTH INTERVAL
C
C     LAMMIN, LAMMAX = LIMITS OF WAVELENGTH INTERVAL IN MICRONS
C     GR = "REFLECTIVITY" (W) OF HAPKE FUNCTION WHICH REPRESENTS GROUND
C     NLAY IS THE NUMBER OF OPTICAL DEPTHS CONSIDERED (NO. OF LAYERS)
C     MAXM = NO. OF FOURIER COEFFICIENTS
C
    3 DO 6 L=1,LE
      DO 6 N=1,NANG
      DO 6 I=1,NUM
      USUM(L,N,I)=0.
    6 DSUM(L,N,I)=0.

      CALL LOADER(DONE)

      IF(LAMMIN.NE.OLAMMIN.AND.OLAMMIN.NE.-99.0) THEN

C     Finished this wavelength.  Write geometric albedoes:
        WRITE(9,5011) OLAMMIN,OLAMMAX,
     & (OLAMMIN+OLAMMAX)*0.5,ALBSAVF/F0SAV,GEOMSAVF/F0SAV
5011  format(5(2X,F6.4))
C
C  Find phase integral Q
C
        Q=ALBSAVF/GEOMSAVF

C        WRITE(8,1009)    ALBSAVF/F0SAV,OLAMMIN,OLAMMAX
C        WRITE(8,5005) GEOMSAVF/F0SAV
5005    format(' GEOMETRIC ALBEDO = ',F8.6)
        WRITE(8,5006) Q
5006    format(' PHASE INTEGRAL = ',F8.5)

C     Write fluxes
        WRITE(8,1010)
        DO 1400 L=1,NLAY-1
	  TAUAC(L)=MUSUN(L)*ALOG(DFDC(1)/DFDC(L))
          WRITE(8,1014) L,ALT(L),TAUAC(L),DFDC(L),
     &    FDC(L),FUC(L),FNETC(L),WC(L),TAUC(L)
1400    CONTINUE
        L=NBOT
	TAUAC(L)=MUSUN(L)*ALOG(DFDC(1)/DFDC(L))
        WRITE(8,1014) L,ALT(L),TAUAC(L),DFDC(L),
     &  FDC(L),FUC(L),FNETC(L)

C     Write intensities
        DO 1250 L = 1,NBOT
          WRITE(8,1020)    MAXM,L,TAUA(L),THETAS(L)
 1020     FORMAT (///,9X,'INTENSITIES (WATTS/SQ.M./STERADIAN) USING',
     1    I3,' FOURIER TERMS AT LEVEL ',I2,/10X,'OPTICAL DEPTH = ',
     1    F10.4,5X,'SOLAR ZENITH ANGLE =',F8.4//
     1    10X,'UPWARD INTENSITIES'//)
          WRITE(8,1021)   (THETA(I),I=1,NUM)
 1021     FORMAT (11X,51F11.4/)

C     PRINT THE TABLE OF INTENSITIES AT ALL AZIMUTH AND ZENITH ANGLES
          DO 115 NA = 1,NANG
  115     WRITE(8,1022)    NA,DPHID(NA),(USUMC(L,NA,I),I=1,NUM)
 1022     FORMAT (2X,I2,1X,0PF5.1,1X,1P51E11.3)
          WRITE(8,1023)
 1023     FORMAT (//10X,'DOWNWARD INTENSITIES'//)
          DO 120 NA = 1,NANG
  120     WRITE(8,1022)    NA,DPHID(NA),(DSUMC(L,NA,I),I=1,NUM)
 1250   CONTINUE

C     Reset all variables which accumulate during a wavelength
        DO 1260 L=1,NBOT
          TAUFRACC(L)=0.
          TAUAC(L)=0.
          DFDC(L)=0.
          FDC(L)=0.
          FUC(L)=0.
          FNETC(L)=0.
          WC(L)=0.
          TAUC(L)=0.
          DO 1270 NA=1,NANG
            DO 1480 I=1,NUM
              USUMC(L,NA,I)=0.
              DSUMC(L,NA,I)=0.
1480        CONTINUE
1270      CONTINUE
1260    CONTINUE

      ENDIF

C     Check if all wavelengths finished:  end of program.
      IF(DONE) then
        CLOSE(8)
C       PAUSE 'Normal exit'
        OPEN(16,FILE='model_done',status='unknown')
        CLOSE(16)
        STOP
      end if

C     Begin the next wavelength interval
      WRITE(6,5007) LAMMIN,LAMMAX
5007  format(' BEGINNING WAVELENGTH INTERVAL ',F10.7,' TO ',F10.7)

1303  IFAC=0
      IF(LAMMIN.EQ.OLAMMIN) IFAC=1
      IF(LAMMIN.NE.OLAMMIN) LAMNO=LAMNO+1
C     SOLAR CONSTANT FOR TITAN (FO = PI*F) IN WATTS/SQ.METER
C     Jupiter:
C     F0 = F0/(5.202561**2)
C     Saturn/Titan
C     F0 = F0/(9.538843**2)
C     Mars
C     F0 = F0/(xxxxxxxx**2)
      WRITE(8,1006)   0.5*(LAMMIN+LAMMAX),GR,NLAY,THETAS(1),F0
      OLAMMIN=LAMMIN
      OLAMMAX=LAMMAX
      OF0=F0
      PI2F0=2.0*PI*F0
C     COMPUTE ALL REQUIRED VALUES OF COSINES OF AZIMUTH ANGLES
      DO 100 NA = 1,NANG
      DO 100 MM = 1,MAXM
  100 FOCOS(NA,MM) = F0*COS((MM-1)* DPHI(NA))

      M = 1
      NBOT = NLAY
  
C     Get the single scattering albedo, optical depth, and the
C     single scattering phase function of all layers.  Also get the
C     reflection function (SA), single-scattered reflection function
C     (SSA) of the ground.  (TA and TSA are not used.)
          
C     MBELOW is maximum M in layers below current level
   11 MBELOW = MLAY(NBOT)
      DO 5 L = 1, NBOT
        CALL STLOAD(1,L,SA,TA,SSA,TSA,W(L),TAU(L))
        CALL PLOAD(L)
        TAUA(L+1)=TAUA(L)+TAU(L)
    5 IF(M.EQ.1)  WRITE(8,1008)    L,W(L), TAU(L)
      IF(M.LE.MLAY(NBOT)) THEN
        CALL STLOAD(M,NBOT,SA,TA,SSA,TSA,W(NBOT),TAU(NBOT))
C		write(8,fmt='(1P11E14.5)') SA
C		close(8)
C        open(9,file='Lambert_s_function.dat')
C		read(9,*) SA
C		do 888 i=1,NUM
C		  do 888 j=1,NUM
C		    SSA(i,j)=SA(i,j)
C			TA(i,j)=0.0
C			TSA(i,j)=0.0
C  888   continue
C        close(9)
      ELSE
        DO 9 I=1,NUM
          DO 9 J=I,NUM
            SA(I,J)=0.0
            SA(J,I)=0.0
            SSA(I,J)=0.0
            SSA(J,I)=0.0
    9   CONTINUE
      ENDIF
            
C     WRITE(8,1017)    M,M-1
C1017 FORMAT (/ ' M =',I3,10X,I3,'TH ORDER COEFFICIENT'/)
1017  FORMAT (' M =',I3,10X,I3,' = MAXM'/)
C     INITIALIZE SO(NBOT,I,J), SS0(NBOT,I,J), AND SB(I,J)
      DO 10 I = 1, NUM
        DO 10 J = I,NUM
C       Hapke scaling for W goes here.
          SO(NBOT,I,J) = SA(I,J)
          SO(NBOT,J,I) = SA(J,I)
          SSO(NBOT,I,J) = SSA(I,J)*EXP(-TAUA(NBOT)*(1./MU(J)))
          SSO(NBOT,J,I) = SSA(J,I)*EXP(-TAUA(NBOT)*(1./MU(I)))
          SB(I,J) = SO(NBOT,I,J)
          SB(J,I) = SO(NBOT,I,J)
   10 CONTINUE

C     ADDUP THROUGH ATMOSPHERE SAVING RESULTS
      DO 15 L = 1,NLAY-1
      LEV = NLAY-L
      IF(M.LE.MLAY(LEV)) CALL STLOAD(M,LEV,SA,TA,SSA,TSA,W(LEV),
     & TAU(LEV))
      IF(M.LE.MLAY(LEV).OR.M.LE.MBELOW) THEN
C     One layer has M
        IF(M.LE.MLAY(LEV).AND.M.LE.MBELOW) THEN
C     Both have this M
          CALL ADDUP(TAU(LEV),SA,TA,SB,M)
C     Add as usual
          DO 16 I=1,NUM
          DO 16 J=1,NUM
16        SSO(LEV,I,J) = SSO(LEV+1,I,J)*EXP(-TAU(LEV)/MU(I)) +
     &                   SSA(I,J)*EXP(-TAUA(LEV)*(1./MU(J)))
        ELSE
C     Only one has this coefficient
          IF(MLAY(LEV).GT.MBELOW) THEN
C     If top, simply use S of top
            DO 71 I=1,NUM
            DO 71 J=1,NUM
            SSO(LEV,I,J) = SSA(I,J)*EXP(-TAUA(LEV)*(1./MU(J)))
71          SB(I,J)=SA(I,J)
C     Update number of coefficients in stuff below
            MBELOW = MLAY(LEV)
          ELSE
C     If bottom
            DO 72 I=1,NUM
            DO 72 J=1,NUM
            SSO(LEV,I,J) = SSO(LEV+1,I,J)*EXP(-TAU(LEV)/MU(I))
72          SB(I,J)=SB(I,J)*EXP(-TAU(LEV)*(1./MU(I)+1./MU(J)))
          ENDIF
        ENDIF
      ELSE
C     Neither layer has this coefficient, so zero fill the added S
        DO 70 I=1,NUM
        DO 70 J=1,NUM
        SSO(LEV,I,J) = 0.
70      SB(I,J)=0.
      ENDIF
      DO 15 I = 1,NUM
      DO 15 J = 1,NUM
15    SO(LEV,I,J) = SB(I,J)

      IF (M.EQ.1) THEN
C     COMPUTE SPHERICAL ALBEDO AT LEVEL 1
        SALBEDO = 0.0
        DO 20 I = 1,NUM
        DO 20 J = 1,NUM
   20   SALBEDO = SALBEDO + SO(1,I,J)*WT(I)*WT(J)
C       WRITE(8,1009)    SALBEDO,LAMMIN,LAMMAX

C     THIS SECTION ACCUMULATES THE SPHERICAL ALBEDO FOR THIS WAVELENGTH
C     ALTHOUGH NOTHING IS CURRENTLY DONE WITH THE VALUES
        IF(IFAC.EQ.0) THEN
          F0SAV=F0
          ALBSAVF=SALBEDO*F0
        ELSE
          F0SAV=F0SAV+F0
          ALBSAVF=ALBSAVF+SALBEDO*F0
        ENDIF
      ENDIF

C     SAVE S FUNCTIONS FOR LATER GEOMETRIC ALBEDO CALCULATION
      DO 1280 I=1,NUM
      SM(M,I)=SO(1,I,I)
      SSM(M,I)=SSO(1,I,I)
1280  CONTINUE

C     EVALUATE UI, DI AT TOP OF ATMOSPHERE
      PI4 = 4.0*PI
      DO 25 I = 1,NUM
      DO 25 J = 1,NUM
      UIS(I,J) = SSO(1,I,J)/(PI4*MU(I))
      UI(I,J) = SO(1,I,J)/(PI4*MU(I))
   25 DI(I,J) = 0.0

C     INTERPOLATE FOR UI AT THE REQUIRED SOLAR ZENITH ANGLE
      DO 27 I=1,NUM
      DISUN(I)=0.
      DO 26 J=1,NUM
      UISTEMP(J) = UIS(I,J)
26    UITEMP(J)=UI(I,J)
      CALL LAGRN2(MU,UISTEMP,NUM,MUSUN(I),UISSUN(I))
27    CALL LAGRN2(MU,UITEMP,NUM,MUSUN(I),UISUN(I))

C     FIND DIFFUSE INTENSITIES AT LEVEL 1
      LEV = 1
      DO 105 NA = 1,NANG
      DO 105 I = 1,NUM
      USUM(LEV,NA,I) = USUM(LEV,NA,I) + FOCOS(NA,M)*(UISUN(I) -
     & UISSUN(I))
  105 DSUM(LEV,NA,I) = 0.

      IF (M.EQ.1) THEN
C     EVALUATE FLUXES AT LEVEL 1
C     DIFFUSE UPWARD AND DOWNWARD FLUXES
        FD(LEV) = 0
        FU(LEV) = 0
        DO 30 I = 1,NUM
        WTMU(I) = WT(I)*MU(I)
   30   FU(LEV) = FU(LEV) + UISUN(I)*WTMU(I)
        PI2FO = PI*2.0*F0
        FU(LEV) = FU(LEV)*PI2FO
        DFD(LEV) = F0*MUSUN(LEV)
        FNET(LEV) = DFD(LEV) + FD(LEV) - FU(LEV)
      ENDIF
C  31 WRITE(8,1016)    LEV
C     WRITE(8,1011)    (UISUN(I),I=1,NUM),(DISUN(I),I=1,NUM)

C     INITIALIZE FOR CALCULATIONS AT LEVEL 2
      LEV = 2
      MABOVE = MLAY(1)
      IF(M.LE.MLAY(1)) THEN
        CALL STLOAD(M,1,SAO,TAO,SSAO,TSAO,W(1),TAU(1))
      ELSE
        DO 34 I=1,NUM
        DO 34 J=1,NUM
        SSAO(I,J)=0.
        TSAO(I,J)=0.
        SAO(I,J)=0.
34      TAO(I,J)=0.
      ENDIF
      DO 35 I = 1, NUM
      DO 35 J = 1,NUM
      STO(1,I,J) = TSAO(I,J)
   35 SAI(I,J) = SAO(I,J)

C     LOOP OVER LEVELS BEGINS HERE
   36 DO 37 I = 1,NUM
      DO 37 J = 1,NUM
   37 SB(I,J) = SO(LEV,I,J)
      CALL BETWEEN (0.,TAUA(LEV),0.,0.,SAI,TAO,SB,DI,UI)

      DO 39 I=1,NUM
      DO 38 J=1,NUM
      UISTEMP(J) = SSO(LEV,I,J)/(PI4*MU(I))
      DISTEMP(J) = STO(LEV-1,I,J)/(PI4*MU(I))
      UITEMP(J)=UI(I,J)
38    DITEMP(J)=DI(I,J)
      CALL LAGRN2(MU,UISTEMP,NUM,MUSUN(LEV),UISSUN(I))
      CALL LAGRN2(MU,DISTEMP,NUM,MUSUN(LEV),DISSUN(I))
      CALL LAGRN2(MU,UITEMP,NUM,MUSUN(LEV),UISUN(I))
39    CALL LAGRN2(MU,DITEMP,NUM,MUSUN(LEV),DISUN(I))

      IF (M.EQ.1) THEN
        FD(LEV) = 0
        FU(LEV) = 0
        DO 40 I = 1,NUM
        FD(LEV) = FD(LEV) + DISUN(I)*WTMU(I)
   40   FU(LEV) = FU(LEV) + UISUN(I)*WTMU(I)
        FD(LEV) = FD(LEV)*PI2FO
        FU(LEV) = FU(LEV)*PI2FO
        DFD(LEV) = F0*MUSUN(LEV)*EXP(-TAUA(LEV)/MUSUN(LEV))
        FNET(LEV) = DFD(LEV) + FD(LEV) - FU(LEV)
      ENDIF
      DO 110 NA = 1,NANG
      DO 110 I = 1,NUM
      DSUM(LEV,NA,I) = DSUM(LEV,NA,I) + FOCOS(NA,M)*(DISUN(I)-DISSUN(I))
  110 USUM(LEV,NA,I) = USUM(LEV,NA,I) + FOCOS(NA,M)*(UISUN(I)-UISSUN(I))
C     WRITE(8,1016)    LEV
C     WRITE(8,1011)    (UISUN(I),I=1,NUM),(DISUN(I),I=1,NUM)
C     Test if done with layers
      IF (LEV.EQ.NBOT) GO TO 45

      IF(M.LE.MLAY(LEV)) CALL STLOAD(M,LEV,SB,TB,SSB,TSB,W(LEV),
     &                   TAU(LEV))
      IF(M.LE.MLAY(LEV).OR.M.LE.MABOVE) THEN
C     One layer has M
        IF(M.LE.MLAY(LEV).AND.M.LE.MABOVE) THEN
C     Both have M
          CALL ADDDN(TAUA(LEV),SAO,SAI,TAO,TAU(LEV),SB,TB,M)
          DO 17 I=1,NUM
          DO 17 J=1,NUM
17        STO(LEV,I,J) = STO(LEV-1,I,J)*EXP(-TAU(LEV)/MU(I)) +
     &                   TSB(I,J)*EXP(-TAUA(LEV)/MU(J))
        ELSE
C     One of the two layers is missing coefficient M
          IF(M.GT.MABOVE) THEN
C     Which one?  Top?
            DO 111 I=1,NUM
            DO 111 J=1,NUM
            STO(LEV,I,J) = TSB(I,J)*EXP(-TAUA(LEV)/MU(J))
            SAO(I,J)=SB(I,J)*EXP(-TAUA(LEV)*(1./MU(I)+1./MU(J)))
            SAI(I,J)=SB(I,J)
111         TAO(I,J)=TB(I,J)*EXP(-TAUA(LEV)*(1./MU(J)))
            MABOVE = MLAY(LEV)
          ELSE
C     No, must be bottom.
            DO 112 I=1,NUM
            DO 112 J=1,NUM
            STO(LEV,I,J) = STO(LEV-1,I,J)*EXP(-TAU(LEV)/MU(I))
            SAI(I,J)=SAI(I,J)*EXP(-TAU(LEV)*(1./MU(I)+1./MU(J)))
112         TAO(I,J)=TAO(I,J)*EXP(-TAU(LEV)*(1./MU(I)))
          ENDIF
        ENDIF
      ELSE
C     Neither layer has coefficient M
        DO 113 I=1,NUM
        DO 113 J=1,NUM
        STO(LEV,I,J) = 0.
        SAO(I,J)=0.
        SAI(I,J)=0.
113     TAO(I,J)=0.
      ENDIF

      LEV = LEV  + 1
C     Go do next layer
      GO TO 36

45    IF(M.EQ.1) THEN
C       WRITE(8,1010)
        DO 51 L = 1,NBOT
C       WRITE(8,1014)    L,TAUA(L)/TAUA(NBOT),TAUA(L),DFD(L),FD(L),
C    &  FU(L),FNET(L),W(L),TAU(L)

C     Save cumulative flux parameters until wavelengths change
        TAUFRACC(L) = TAUFRACC(L) + TAUA(L)/TAUA(NBOT)
        TAUAC(L) = TAUAC(L) + TAUA(L)
        DFDC(L) = DFDC(L) + DFD(L)
        FDC(L) = FDC(L) + FD(L)
        FUC(L) = FUC(L) + FU(L)
        FNETC(L) = FNETC(L) + FNET(L)
        WC(L) = WC(L) + W(L)
        TAUC(L) = TAUC(L) + TAU(L)
51      CONTINUE
C       WRITE(8,1014)   NBOT,TAUA(NBOT)/TAUA(NBOT),TAUA(NBOT),DFD(NBOT),
C    &  FD(NBOT),FU(NBOT),FNET(NBOT)
      ENDIF
      IF (M .LT. MAXM) THEN
        M = M + 1
C       WRITE(8,1017)    M,M-1
C       WRITE(6,1017)    M,MAXM
C     Do next coefficient
        GO TO 11
      ENDIF

C     FOURIER SERIES COMPUTATION FINISHED, HAVE RELATIVE UP AND DOWN
C     INTENSITIES FOR ALL DESIRED VALUES OF PHI-PHI(0)
C     LOOP TO PRINT UP AND DOWN DIFFUSE INTENSITIES AT ALL LAYERS FOR
C     THIS WAVELENGTH.
C
C  Compute Geometric Albedo
C
C     open(16,file='geomdebug.out')
      GEOM=0.
      DO 1245 I=1,NUM
      GM=0.
      FACT=1.
      DO 1240 M=1,MAXM
      GM=GM+(SM(M,I)-SSM(M,I))*FACT
C     write(16,5020) I,M,SM(M,I),SSM(M,I)
C    & 1pg11.3)
C5020  format('I = ',i2,' M = ',i2,' SM = ',1pg11.3,' SSM = ',
1240  FACT=-FACT
      SINGLE=SSS(MU(I),MU(I),180.,TAU,W,TAUA,GR,1,NBOT,HAPKE_B0,
     &  HAPKE_B,HAPKE_C,HAPKE_H)
      GEOM=GEOM+0.5*(SINGLE+GM)*WT(I)
C      write(6,5021) I,MU(I),SINGLE,GEOM
C5021  format('I = ',i2,' MU = ',f8.6,' SINGLE = ',1pg11.3,' GEOM = ',
C     & 1pg11.3)
1245  CONTINUE
C     close(16)
C     pause
C     stop
C     THIS SECTION ACCUMULATES THE GEOMETRIC ALBEDO FOR THIS WAVELENGTH
      IF(IFAC.EQ.0) THEN
        GEOMSAVF=GEOM*F0
      ELSE
        GEOMSAVF=GEOMSAVF+GEOM*F0
      ENDIF

      DO 125 L = 1,NBOT
C     WRITE(8,1020)    MAXM,L,TAUA(L),THETAS(L)
C1020 FORMAT (///,9X,'INTENSITIES (WATTS/SQ.M./STERADIAN) USING',
C    1  I3,' FOURIER TERMS AT LEVEL ',I,/10X,'OPTICAL DEPTH = ',
C    1  F10.4,5X,'SOLAR ZENITH ANGLE =',F8.4//
C    1  10X,'UPWARD INTENSITIES'//)
C     WRITE(8,1021)   (THETA(I),I=1,NUM)
C1021 FORMAT (11X,11F11.4/)

C     Add single scattering component
      DO 200 I=1,NUMG
      DO 200 NA=1,NANG
      USUM(L,NA,I) = USUM(L,NA,I) + SSS(MU(I),MUSUN(L),DPHID(NA),TAU,
     & W,TAUA,GR,L,NBOT,HAPKE_B0,HAPKE_B,HAPKE_C,HAPKE_H)/(4.*MU(I))*
     & F0/PI
      DSUM(L,NA,I) = DSUM(L,NA,I) + SST(MU(I),MUSUN(L),DPHID(NA),TAU,
     & W,TAUA,L,NBOT)/(4.*MU(I))*F0/PI
      USUMC(L,NA,I) = USUMC(L,NA,I) + USUM(L,NA,I)
      DSUMC(L,NA,I) = DSUMC(L,NA,I) + DSUM(L,NA,I)
200   CONTINUE

C     PRINT THE TABLE OF INTENSITIES AT ALL AZIMUTH AND ZENITH ANGLES
C     DO 115 NA = 1,NANG
C 115 WRITE(8,1022)    NA,DPHID(NA),(USUM(L,NA,I),I=1,NUM)
C1022 FORMAT (2X,I2,1X,0PF5.1,1X,1P11E11.3)
C     WRITE(8,1023)
C1023 FORMAT (//10X,'DOWNWARD INTENSITIES'//)
C     DO 120 NA = 1,NANG
C 120 WRITE(8,1022)    NA,DPHID(NA),(DSUM(L,NA,I),I=1,NUM)
  125 CONTINUE

      GO TO 3
      END
      SUBROUTINE ADDDN(TAUA,SAO,SAI,TAO,TAUB,SB,TB,NCO)
C     SUBROUTINE TO COMPUTE S,T FUNCTIONS (FOR A GIVEN FOURIER
C     ORDER) RESULTING FROM THE ADDITION OF A HOMOGENEOUS LAYER BELOW
C     AN INHOMOGENEOUS LAYER.
      PARAMETER (NUMG=64)
      REAL MU
      COMMON N,NMAX,SCRIT,MU(NUMG),WT(NUMG),HWTOM(NUMG),QWTOM(NUMG)
      DIMENSION SAI(NUMG,NUMG), SAO(NUMG,NUMG), TAO(NUMG,NUMG),
     & SB(NUMG,NUMG), TB(NUMG,NUMG), SIGOO(NUMG,NUMG), SIGOI(NUMG,NUMG),
     & SIGEO(NUMG,NUMG), SLN(NUMG,NUMG), SLNI(NUMG,NUMG),
     & SLAST(NUMG,NUMG), SL2(NUMG,NUMG)
      DIMENSION PT5(NUMG,NUMG), PT5O(NUMG,NUMG), TAOH(NUMG,NUMG),
     & TBH(NUMG,NUMG)
      DIMENSION HWTOMU(NUMG), ETAUA(NUMG),ETAUB(NUMG)
      DIMENSION QOE(2) , QEO(2) , DOE(2), DEO(2)
 !     EQUIVALENCE (PT5(1),SLN(1)),(PT5O(1),SLNI(1)),(TAOH(1),SLAST(1)),
 !    1 (TBH(1),SL2(1))
    8 FORMAT(//5X, 3HSAO,20X,23H ORDER OF COEFFICIENT =  , I3)
    9 FORMAT(1X, 1P11E11.4)
   10 FORMAT(/5X, 3HTAO)
   13 FORMAT(5X, 15HSCRIT SATISFIED, 5X, 2I5)
   14 FORMAT(5X, 19HSCRIT NOT SATISFIED , 5X, 2I5)
   15 FORMAT(5X,8HQEO(K) = , E16.8, 8HDEO(K) = , E16.8, 5X,I5,5X,E16.8)
   16 FORMAT(5X,8HQOE(K) = , E16.8, 8HDOE(K) = , E16.8, 5X,I5,5X,E16.8)
   20 FORMAT(/5X, 6HBOUNCE  )
   22 FORMAT(//5X, 11HTOTAL TAU = , F7.3)
   28 FORMAT(/5X, 3HSAI)
   29 FORMAT(/5X, I5)
      IN = N/2
      IP1 = 1
      IP1 = 0
      IP2 = 1
      IP2 = 0
      IF(NCO.NE.1) GO TO 1103
      DO 999 I = 1, N
  999 HWTOMU(I) = HWTOM(I)
      GO TO 1105
 1103 DO 1104 I = 1,N
 1104 HWTOMU(I) = QWTOM(I)
 1105 CONTINUE
      IF(IP1.NE.0) WRITE(8,20)
C**********************************************************************
C       NOTE:  THIS SECTION TREATS TWO CASES OF PURE ABSORPTION:
C               1.  SB(I,J) = 0.
C               2.  SAO(I,J) AND SAI(I,J) = 0.
C       (ADDED BY TOMASKO AND DOOSE (11/20/78))
      DO 99 I=1,N
      ETAUA(I) = EXP(-TAUA/MU(I))
   99 ETAUB(I) = EXP(-TAUB/MU(I))
      DO 30 I=1,N
      DO 30 J=1,N
   30 IF(SB(I,J).GE.1.0E-15) GO TO 32
      DO 31 I=1,N
      DO 31 J=1,N
C     SAO IS UNCHANGED.
      SAO(I,J)=SAO(I,J)
C     BUT SAI IS ATTENUATED BY PURE ABSORPTION.
      SAI(I,J)=ETAUB(I)*ETAUB(J)*SAI(I,J)
C     TAO IS ATTENUATED BY PURE ABSORPTION OF THE EXIT BEAM ONLY.
   31 TAO(I,J)= TAO(I,J)*ETAUB(I)
      GO TO 156

C     NOW TREAT THE CASE WHERE SAO(I,J) AND SAI(I,J) = 0.
   32 DO 33 I=1,N
      DO 33 J=1,N
   33 IF(SAO(I,J).GE.1.0E-15.OR.SAI(I,J).GE.1.0E-15) GO TO 131
      DO 34 I=1,N
      DO 34 J=1,N
      SAO(I,J)=ETAUA(I)*ETAUA(J)*SB(I,J)
      SAI(I,J)=SB(I,J)
   34 TAO(I,J)=ETAUA(I)*TB(I,J)
      GO TO 156
C**********************************************************************

C           INITIALIZE SLAST, SIGO, SIGE
C      COMPUTE S SUB 2
  131 DO 135 I = 1,N
      DO 135 J = 1,N
      SL2(I,J) = 0.
      DO 134 K = 1,N
  134 SL2(I,J) = SL2(I,J) + HWTOMU(K)*SAI(I,K) * SB(K,J)
  135 SIGEO(I,J) = SL2(I,J)
      NEMAX = 2
      IF(IP2.NE.0) WRITE(8,9)   SL2
      QEO(1) = SL2(N,N)/SB(N,N)
      QEO(2) = SL2(IN,N)/SB(IN,N)

      IF(QEO(1)+QEO(2).GT.2.0E-15) GO TO 130
      DO 141 I=1,N
      DO 141 J=1,N
      SIGOI(I,J)=SAI(I,J)
      SIGOO(I,J)=SB(I,J)
141   SIGEO(I,J)=SL2(I,J)
      GO TO 152

C      COMPUTE S SUB 3
130   DO 137 I = 1,N
      DO 137 J = I,N
      SLAST(I,J) = 0.
      SLNI(I,J) = 0.
      DO 136 K = 1,N
      SLNI(I,J) = SLNI(I,J) + HWTOMU(K) * SL2(J,K) * SAI(K,I)
  136 SLAST(I,J) = SLAST(I,J) + HWTOMU(K)*SB(I,K)*SL2(K,J)
      SLAST(J,I) = SLAST(I,J)
      SLNI(J,I) = SLNI(I,J)
      SIGOO(I,J) = SB(I,J)
      SIGOI(I,J) = SAI(I,J)
      SIGOO(J,I) = SIGOO(I,J)
  137 SIGOI(J,I) = SIGOI(I,J)
      NOMAX = 3
      IF(IP2.NE.0) WRITE(8,29)   NOMAX
      IF(IP2.NE.0) WRITE(8,9)   SLAST
      IF(IP2.NE.0) WRITE(8,9)   SLNI
      QOE(1) = SLAST(N,N)/SL2(N,N)
      QOE(2) = SLAST(IN,N)/SL2(IN,N)

C         LOOP AND TEST RATIO OF TERMS UP TO NMAX TIMES
      GO TO 200

C         RETURN HERE IF SCRIT SATISFIED BEFORE REACH NMAX
  138 IF(IP1.NE.0) WRITE(8,13)   NEMAX,NOMAX
      GO TO 140

C       RETURN HERE IF SCRIT NOT SATISFIED AFTER NMAX INTEGRATIONS
  139 IF(IP1.NE.0) WRITE(8,14)   NEMAX,NOMAX
  140 IF(NEO) 143,143,148
  143 DO 146 I=1,N
      DO 146 J=1,N
        IF(SL2(I,J).EQ.0.0) GO TO 146
      R = SLN(I,J)/SL2(I,J)
      RFACT = 1./(1.-R)
      SIGOO(I,J) = SIGOO(I,J) + SLAST(I,J)*RFACT
      SIGEO(I,J) = SIGEO(I,J) +  SLN(I,J)*RFACT
      SIGOI(I,J) = SIGOI(I,J) + SLNI(I,J)*RFACT
  146 CONTINUE
      GO TO 300
  148 DO 151 I= 1,N
      DO 151 J=1,N
      IF(SL2(I,J).EQ.0.0) GO TO 152
      R = SLN(I,J)/SL2(I,J)
      RFACT = 1./(1.-R)
      SIGOO(I,J) = SIGOO(I,J) + SLN(I,J) * RFACT
      SIGEO(I,J) = SIGEO(I,J) +  SLAST(I,J) * RFACT
  151 SIGOI(I,J) = SIGOI(I,J) + SLNI(I,J) * RFACT

C        EVALUATE  SAI(MU,MU0),  SAO(MU,MU0)
  152 GO TO 300
  153 TAUT = TAUA + TAUB
      IF(IP1.EQ.0) GO TO 155
      WRITE(8,22)   TAUT
      WRITE(8,8)    NCO
      WRITE(8,9)   ((SAO(I,J),I=1,N),J=1,N)
      WRITE(8,28)
      WRITE(8,9)   ((SAI(I,J),I=1,N),J=1,N)

C         EVALUATE TAO(MU,MU0)
  155 GO TO 400
  156 IF(IP1.EQ.0) GO TO 157
      WRITE(8,10)
      WRITE(8,9)   ((TAO(I,J),I=1,N),J=1,N)
  157 CONTINUE
      RETURN

C      LOOP AND TEST FOR SIGO AND SIGE
  200 DO 241 K=4,NMAX, 2

C        EVEN S SUB N COMPUTATION
      NEO = 0
      NEMAX = NEMAX + 2

C      EVEN S SUB N INTEGRAL
      DO 205 I = 1, N
      DO 205 J = 1,N
      SLN(I,J)=0.
      DO 205 L=1,N
  205 SLN(I,J) = SLN(I,J) + HWTOMU(L)*SAI(I,L)*SLAST(L,J)
      IF(IP2.EQ.0) GO TO 207
      WRITE(8,9)   ((SLN(I,J), I=1,N),J=1,N)

C            TEST FOR CONSTANT RATIO
  207 DEO(1) = QEO(1)
      DEO(2) = QEO(2)
        IF(SLAST(N,N).EQ.0.0.OR.SLAST(IN,N).EQ.0.0) GO TO 138
      QEO(1) = SLN(N,N)/SLAST(N,N)
      QEO(2) = SLN(IN,N)/SLAST(IN,N)
      AM= (QEO(1)/DEO(1) + QEO(2)/DEO(2))*0.5-1.
      IF(IP1.EQ.0) GO TO 213
      WRITE(8,15)   QEO(1),DEO(1), NEMAX, AM
      WRITE(8,15)   QEO(2) , DEO(2)
  213 IF(AM) 214,215,215
  214 AM = -AM
  215 IF(AM-SCRIT) 138,138,216

C     IF DID NOT SATISFY SCRIT TEST FOR EVEN S SUB N
  216 DO 220 I=1,N
      DO 220 J=1,N
      SL2(I,J) = SLAST(I,J)
      SLAST(I,J) = SLN(I,J)
      SIGOO(I,J) = SIGOO(I,J) + SL2(I,J)
  220 SIGOI(I,J) = SIGOI(I,J) + SLNI(I,J)

C       ODD S SUB N COMPUTATION  ( SLN   = S SUB N)
      NEO = 1
      NOMAX = NOMAX + 2

C        ODD S SUB N INTEGRAL
      DO 227 I = 1,N
      DO 227 J = 1,N
      SLN(I,J) = 0.
      SLNI(I,J) = 0.
      DO 226 L=1,N
      SLNI(I,J) = SLNI(I,J) + HWTOMU(L)*SLAST(J,L)*SAI(L,I)
  226 SLN(I,J) = SLN(I,J) + HWTOMU(L)*SB(I,L)*SLAST(L,J)
  227 CONTINUE
      IF(IP2.EQ.0) GO TO 228
      WRITE(8,9)   ((SLN(I,J), I=1,N),J=1,N)
      WRITE(8,9)   ((SLNI(I,J), I=1,N),J=1,N)

C              TEST FOR CONSTANT RATIO
  228 DOE(1) = QOE(1)
      DOE(2) = QOE(2)
        IF(SLAST(N,N).EQ.0.0.OR.SLAST(IN,N).EQ.0.0) GO TO 138
      QOE(1) = SLN(N,N)/SLAST(N,N)
      QOE(2) = SLN(IN,N)/SLAST(IN,N)
      AM=(QOE(1)/DOE(1) + QOE(2)/DOE(2))*0.5-1.
      IF(IP1.EQ.0) GO TO 233
      WRITE(8,16)   QOE(1), DOE(1) , NOMAX,AM
      WRITE(8,16)   QOE(2) , DOE(2)
  233 IF(AM) 234,235,235
  234 AM = -AM
  235 IF(AM-SCRIT) 138,138,236

C     IF DID NOT SATISFY SCRIT TEST FOR ODD TERM
  236 IF(K-NMAX)237,241,241
  237 DO 240 I=1,N
      DO 240 J=1,N
      SL2(I,J) = SLAST(I,J)
      SLAST(I,J) = SLN(I,J)
  240 SIGEO(I,J) = SIGEO(I,J) + SL2(I,J)
  241 CONTINUE
      GO TO 139

C       EVALUATE SAI(MU,MU0), SAO(MU,MU0)
  300 DO 303 I = 1, N
      DO 303 J = 1, N
      TAOH(I,J) = TAO(I,J)*HWTOMU(I)
  303 TBH(I,J) = TB(I,J) * HWTOMU(I)
      DO 310 I = 1,N
      DO 310 J = 1,N
      PT5(I,J) = 0.
      PT5O(I,J) = 0.
      DO 310 K = 1,N
      PT5(I,J) = PT5(I,J) + SIGOI(I,K)*TBH(K,J)
  310 PT5O(I,J) = PT5O(I,J) + SIGOO(I,K)*TAOH(K,J)
      DO 327 I = 1,N
      DO 327 J = I,N
      T5 = 0.
      T5O = 0.
      DO 317 K = 1,N
      T5 = T5 + TBH(K,I)*PT5(K,J)
  317 T5O   = T5O + TAOH(K,I)*PT5O(K,J)
      T4 = PT5(I,J)*ETAUB(I)
      T4O = PT5O(I,J)*ETAUA(I)
      T3 = PT5(J,I)*ETAUB(J)
      T3O = PT5O(J,I)*ETAUA(J)
      T2 = SIGOI(I,J)*ETAUB(I)*ETAUB(J)
      T2O = SIGOO(I,J)*ETAUA(I)*ETAUA(J)
      SAI(I,J) =  SB(I,J) + T2 + T3 + T4 + T5
      SAI(J,I) = SAI(I,J)
      SAO(I,J) = SAO(I,J) + T2O + T3O + T4O + T5O
  327 SAO(J,I) = SAO(I,J)
      GO TO 153

C    EVALUATE TAO(MU,MU0)
  400 DO 418 I = 1,N
      DO 404 J = 1,N
      PT5(I,J) = 0.
      DO 404 K = 1,N
  404 PT5(I,J) = PT5(I,J) + SIGEO(K,J) * TBH(K,I)
      DO 418 J = 1,N
      T4 = 0.
      PT6 = 0.
      T7 = 0.
      DO 412 K = 1,N
      T4 = T4 + TB(I,K) * TAOH(K,J)
      PT6 = PT6 + SIGEO(I,K) * TAOH(K,J)
  412 T7 = T7 + PT5(I,K)*TAOH(K,J)
      T6 = ETAUB(I)*PT6
      T5 = ETAUA(J) * PT5(I,J)
      T3 =SIGEO(I,J)*ETAUA(J)*ETAUB(I)
      T2 =TAO(I,J) * ETAUB(I)
      T1 = TB(I,J)*ETAUA(J)
  418 TAO(I,J) = T1 + T2 + T3 + T4 + T5 + T6 + T7
      GO TO 156
      END
      SUBROUTINE ADDUP(TAUA,SA,TA,SB,M)
C     SUBROUTINE TO COMPUTE S FUNCTION RESULTING FROM THE ADDITION
C     OF A HOMOGENEOUS LAYER OF THICKNESS TAUA CHARACTERIZED BY SA,TA,
C     ABOVE AN INHOMOGENEOUS LAYER CHARACTERIZED BY SB WHEN ILLUMINATED
C     FROM ABOVE.  THE RESULTING S FUNCTION FOR THE COMPOSITE OF THE
C     TWO LAYERS FOR ILLUMINATION FROM ABOVE IS RETURNED IN SB.
C     ALL FUNCTIONS REFER TO FOURIER ORDER M-1.
C     SECOND SUBSCRIPT(J) REFERS TO INCIDENT DIRECTION,FIRST
C     SUBSCRIPT(I) TO EMERGENT DIRECTION.
      PARAMETER (NUMG=64)
      COMMON N,NMAX,SCRIT,XMU(NUMG),WT(NUMG),HWTOMU(NUMG),QWTOMU(NUMG)
      DIMENSION SA(NUMG,NUMG), TA(NUMG,NUMG),SB(NUMG,NUMG),
     & SIGO(NUMG,NUMG), SLAST(NUMG,NUMG), SBSA(NUMG,NUMG),SN(NUMG,NUMG),
     & ETAUA(NUMG), PT5(NUMG,NUMG), TAWT(NUMG,NUMG), WTOMU(NUMG)
C      EQUIVALENCE (PT5(1),SN(1)),(TAWT(1),SLAST(1))
C      IP1 = 1
      IP1 = 0
C      IP2 = 1
      IP2 = 0
      DO 6 I = 1,N
      DO 6 J = 1,N
    6 IF (SB(I,J) .EQ. 0.0) GO TO 5
      GO TO 8
    5 DO 7 I = 1,N
      DO 7 J = 1,N
    7 SB(I,J) = SA(I,J)
      GO TO 321
    8 IN = N / 2
      IF (M.NE.1) GO TO 15
      DO 10 I=1,N
   10 WTOMU(I) = HWTOMU(I)
      GO TO 25
   15 DO 20 I=1,N
   20 WTOMU(I) = QWTOMU(I)
   25 IF(IP1.NE.0) WRITE(8,30)
   30 FORMAT(/,5X,6HBOUNCE)
      DO 32 I = 1,N
      TEMP = TAUA/XMU(I)
      IF(TEMP.GT.100.0) ETAUA(I) = 0.0
   32 IF(TEMP.LE.100.0) ETAUA(I) = EXP(-TEMP)

C**********************************************************************
C       NOTE:  THIS SECTION TREATS THE CASE WHERE SA(I,J) = 0.
C              IN THAT CASE THERE IS NO SCATTERING, BUT ONLY PURE
C              ABSORPTION. (ADDED BY TOMASKO AND DOOSE, 11/20/78)
      DO 33 I=1,N
      DO 33 J=1,N
   33 IF(SA(I,J).NE.0.0) GO TO 34
      DO 31 I=1,N
      DO 31 J=1,N
   31 SB(I,J)=ETAUA(I)*ETAUA(J)*SB(I,J)
      GO TO 321
C**********************************************************************

C     COMPUTE SBSA INTEGRAL, INITIALIZE SN, SIGO,Q1,Q2, NT
   34 DO 40 I= 1,N
      DO 40 J=1,N
      SBSA(I,J) = 0.
      DO 35 K=1,N
   35 SBSA(I,J) = SBSA(I,J) + SB(I,K)*SA(K,J)*WTOMU(K)
      SN(I,J) = SB(I,J)
   40 SIGO(I,J) = 0.0
    9 FORMAT(1X,"SBSA ",(1P11E12.5))
      IF (IP2.NE.0) WRITE(8,9) SBSA
      Q1 = 0.
      Q2 = 0.
      NT = 1
C      COMPUTE SN(NT) WITH NT ODD
   44 NT = NT + 2
      NGG = 1
      DO 50 I = 1,N
      DO 50 J = I,N
      SIGO(I,J) = SIGO(I,J) + SN(I,J)
      SLAST(I,J) = SN(I,J)
   50 SLAST(J,I) = SLAST(I,J)
      DO 49 I = 1,N
      DO 49 J = I,N
      SN(I,J) = 0.0
      DO 45 K = 1,N
   45 SN(I,J) = SN(I,J) + SBSA(I,K)*SLAST(K,J)*WTOMU(K)
   49 IF(SN(I,J)/ SIGO(I,J).GT.1.0E-07) NGG = 0
      IF (IP2.NE.0) WRITE(8,409)  ((SN(I,J),I=1,N),J=1,N)
  409 FORMAT(1X,"SN ",(1P11E12.5))

C     TEST IF TIME TO STOP EVALUATING TERMS
      D1 = Q1
      D2 = Q2
      Q1 = SN(IN,N)/SLAST(IN,N)
      Q2 = SN(N,N)/SLAST(N,N)
C      IF(NGG.EQ.1) GO TO 98
      IF(NT.LT.5) GO TO 44
      AM = (Q1/D1 + Q2/D2)*0.5 - 1.0
      IF(IP1.EQ.0) GO TO 70
      WRITE(8,60) Q1,D1,NT,AM
      WRITE(8,60) Q2,D2
   60 FORMAT(5X,13HS(N)/S(N-2) =  ,1PE16.8,5X,15HS(N-2)/S(N-4) =  ,
     1  1PE16.8,5X,I5,5X,1PE16.8)
   70 IF(AM.LT.0.0) AM = -AM
      IF(NT.GE. NMAX) GO TO 98
C      IF(AM.GT.SCRIT) GO TO 44
      GO TO 44
   98 IF(IP1.EQ.0 ) GO TO 100
      WRITE(8,99) NT,NGG,AM
   99 FORMAT(5X,4HNT = ,I5, 5X, 5HNGG = , I5,5X,4HAM = ,1PE16.8)

C     APPROXIMATE REST OF SIGO BY GEOMETRIC SERIES.
  100 DO 110 I = 1,N
      DO 110 J = I,N
      BOT = 1.0 - SN(I,J)/SLAST(I,J)
	  IF(IP1.NE.0) WRITE(6,FMT='("BOT = ",F10.5)') BOT
      IF(BOT.GT.0.0) GO TO 103
      WRITE(8,5009)
      WRITE(6,5009)
5009  format(' CONVERGENCE PROBLEM IN ADDUP!')
      WRITE(8,102) NT,I,J,SIGO(I,J), SLAST(I,J), SN(I,J),BOT
  102 FORMAT(2X,3I5,1P4E16.8)
C      CLOSE(8)
	  CONTINUE
C     STOP 'STOP 100'
      BOT=1.0
  103 SIGO(I,J) = SIGO(I,J) + SN(I,J)/BOT
  110 SIGO(J,I) = SIGO(I,J)

C     EVALUATE S(I,J) FOR COMPOSITE LAYERS FOR ILLUMINATION
C     FROM ABOVE.
      DO 305 I = 1,N
      DO 305 J = 1,N
  305 TAWT(I,J) = TA(I,J)*WTOMU(I)
      DO 310 I = 1,N
      DO 310 J= 1,N
      PT5(I,J) = 0.0
      DO 310 K = 1,N
  310 PT5(I,J) = PT5(I,J) + SIGO(I,K)*TAWT(K,J)
      DO 320 I = 1,N
      DO 320 J = I,N
      T5 = 0.0
      DO 315 K = 1,N
  315 T5 = T5 + TAWT(K,I)*PT5(K,J)
      T4 = PT5(I,J)*ETAUA(I)
      T3=PT5(J,I)*ETAUA(J)
      T2=ETAUA(I) * SIGO(I,J)*ETAUA(J)
      SB(I,J) = SA(I,J) + T2 +T3 + T4 + T5
  320 SB(J,I) = SB(I,J)
  321 IF (IP2 .NE. 0) WRITE(8,9) SB
      RETURN
      END
      SUBROUTINE BETWEEN(TAUA,TAUL,TAUB1,TAUB2,SL,TL,SC,DI,UI)
C     COMPUTES UPWARD AND DOWNWARD INTENSITIES, UI(M) AND DI(M), AS SEEN
C     BY AN OBSERVER BETWEEN AN UPPER CLOUD LAYER (L) AND A LOWER CLOUD
C     LAYER (C).  AN ABSORBING GAS LAYER (A) LIES ABOVE THE UPPER CLOUD
C     LAYER AND THE OBSERVER IS WITHIN AN ABSORBING GAS LAYER (B) AT
C     OPTICAL DEPTH TAUB1 BELOW THE UPPER CLOUD LAYER AND OPTICAL DEPTH
C     TAUB2 ABOVE THE LOWER CLOUD LAYER.
C     M IS THE ORDER OF THE FOURIER COEFFICIENT PLUS ONE.
C     J SPECIFIES MU(0), I SPECIFIES MU.
      PARAMETER (NUMG=64)
      COMMON NUM,NMAX,SCRIT,XMU(NUMG),W(NUMG),HWTOMU(NUMG),QWTOMU(NUMG),
     & M
      DIMENSION AX(NUMG), SL(NUMG,NUMG), TL(NUMG,NUMG), SC(NUMG,NUMG)
      DIMENSION DI(NUMG,NUMG), UI(NUMG,NUMG), SIGO(NUMG,NUMG),
     & SIGE(NUMG,NUMG)
      DIMENSION TEMPA(NUMG,NUMG), TEMPB(NUMG,NUMG), TEMPC(NUMG,NUMG)
      DATA  PI, TOL/3.14159265359, 1.0E-5/
      TAUB = TAUB1 + TAUB2
      DO 40 I = 1,NUM
      DO 40 J = 1,NUM
   40 IF (SC(I,J) .NE. 0.0) GO TO 46
      DO 45 J = 1,NUM
      XAO = EXP(-TAUA/XMU(J))
      DO 45 I = 1,NUM
      FORMU = 4.0*PI*XMU(I)
      XB1 = EXP(-TAUB1/XMU(I))
      DI(I,J) =(XAO*XB1/FORMU)*TL(I,J)
   45 UI(I,J) = 0.0
      GO TO 22
   46 IF (M-1) 2,1,2
    1 COEF = 0.5
      GO TO 3
    2 COEF = 0.25
C     COMPUTE SIGO AND SIGE SERIES FROM SCATTERING FUNCTIONS SL AND SC.
    3 DO 4 I=1,NUM
      AX(I) = (W(I)/XMU(I))*EXP(-TAUB/XMU(I))
      DO 4 J=1,NUM
      SIGO(I,J) = SC(I,J)
      SIGE(I,J) = 0.0
    4 TEMPA(I,J) = SC(I,J)
      N = 1
      IP1 = 1
      IP1 = 0
      IF (IP1 .EQ. 0) GO TO 5
      WRITE(8,3000)    N
 3000 FORMAT (//1X,'N =',I5)
      WRITE(8,3001)    SC
 3001 FORMAT (//' S(N)'/(1X,1P11E11.4))
    5 N = N+1
      IF (IP1 .NE. 0) WRITE(8,3000) N
C     COMPUTE EVEN S(N) AND ADD TO THE SIGE SERIES.
C     THE EVEN S(N) AND SIGE ARE NOT SYMMETRIC IN I AND J.
      DO 7 I=1,NUM
      DO 7 J=1,NUM
      SUMX = 0.0
      DO 6 K=1,NUM
    6 SUMX = SUMX + AX(K)*SL(I,K)*TEMPA(K,J)
      TEMPB(I,J) = SUMX*COEF
    7 SIGE(I,J) = SIGE(I,J) + TEMPB(I,J)
      IF (IP1 .NE. 0) WRITE(8,3002) TEMPB
 3002 FORMAT (//' EVEN S(N)'/(1X,1P11E11.4))
C     COMPUTE ODD S(N) AND ADD TO THE SIGO SERIES.
C     THE ODD S(N) AND SIGO ARE SYMMETRIC IN I AND J.
      N = N+1
      IF (IP1 .NE. 0) WRITE(8,3000) N
      NGG = 1
      DO 14 I=1,NUM
      DO 14 J=I,NUM
      SUMX = 0.0
      DO 8 K=1,NUM
    8 SUMX = SUMX + AX(K)*SC(I,K)*TEMPB(K,J)
      TEMPC(I,J) = SUMX*COEF
C     WRITE(6,5077) N,I,J,SIGO(I,J),TEMPC(I,J)
C5077 FORMAT(3I5,2E15.7)
      IF(N-9) 9,11,11
    9 SIGO(I,J) = SIGO(I,J) + TEMPC(I,J)
      SIGO(J,I) = SIGO(I,J)
C     DETERMINE IF IT IS WORTHWHILE TO COMPUTE ANY HIGHER S(N).
        IF(SIGO(I,J).EQ.0.0) GO TO 14
      TEST = ABS(TEMPC(I,J)/SIGO(I,J))
      IF(TEST-TOL) 14,14,10
   10 NGG = 0
      GO TO 14
C     GEOMETRIC SERIES APPROXIMATE TERMINATION AFTER S(9) COMPUTED.
   11 RE = TEMPC(I,J)/TEMPA(I,J)
C     WRITE(6,5077) N,I,J,TEMPC(I,J),TEMPA(I,J),RE
C5077 FORMAT(3I5,3E15.7)
      IF(1.0-RE*RE) 12,12,13
C  12 WRITE(8,120)    I, J, N, TEMPA(I,J), TEMPB(I,J), TEMPC(I,J)
C 120 FORMAT (/10X, 3I5, 3(2X, E13.6))
C     STOP 12
   12 SIGO(I,J) = SIGO(I,J) - TEMPC(I,J)
      SIGO(J,I) = SIGO(I,J)
      GO TO 14
   13 BOT = 1.0-RE
      SIGO(I,J) = SIGO(I,J) + TEMPC(I,J)/BOT
      SIGO(J,I) = SIGO(I,J)
      SIGE(I,J) = SIGE(I,J) + RE*TEMPB(I,J)/BOT
      IF(I-J) 140,14,140
  140 SIGE(J,I) = SIGE(J,I) + RE*TEMPB(J,I)/BOT
   14 CONTINUE
      IF (IP1 .NE. 0) WRITE(8,3003) TEMPC
 3003 FORMAT (//' ODD S(N)'/(1X,1P11E11.4))
      IF(N-9) 15,18,18
   15 IF(NGG) 18,16,18
   16 DO 17 I=1,NUM
      DO 17 J=I,NUM
      TEMPA(I,J) = TEMPC(I,J)
   17 TEMPA(J,I) = TEMPA(I,J)
      GO TO 5
C     COMPUTE INTEGRAL TERMS OF DI AND UI.
   18 DO 20 I=1,NUM
      DO 20 J=1,NUM
      SUMX = 0.0
      SUMY = 0.0
      DO 19 K=1,NUM
C     INTEGRAL FOR DI (WHICH IS NOT SYMMETRIC IN I AND J).
      SUMX = SUMX + AX(K)*TL(K,J)*SIGE(I,K)
C     INTEGRAL FOR UI (WHICH IS SYMMETRIC IN I AND J).
   19 SUMY = SUMY + AX(K)*TL(K,J)*SIGO(I,K)
      TEMPA(I,J) = SUMX*COEF
   20 TEMPB(I,J) = SUMY*COEF
C     COMBINE TERMS TO FORM INTENSITIES DI(M) AND UI(M) (WHICH ARE NOT
C     SYMMETRIC IN I AND J).   THE INTENSITIES ARE RELATIVE TO THE
C     INCIDENT SOLAR FLUX F(0) = PI*F, I.E., MULTIPLICATION OF THESE
C     INTENSITIES BY THE SOLAR FLUX (SOLAR CONSTANT) GIVES ABSOLUTE
C     INTENSITIES IN WHATEVER UNITS ARE USED FOR F(0) = PI*F.
      DO 21 J=1,NUM
      XAO = EXP(-TAUA/XMU(J))
      XLO = EXP(-TAUL/XMU(J))
      XBO = EXP(-TAUB/XMU(J))
      DO 21 I=1,NUM
      FORMU = 4.0*PI*XMU(I)
      XB1 = EXP(-TAUB1/XMU(I))
      XB2 = EXP(-TAUB2/XMU(I))
      DI(I,J) = ((XAO*XB1)/FORMU)*(TL(I,J) + XLO*XBO*SIGE(I,J)
     1+ TEMPA(I,J))
   21 UI(I,J) = ((XAO*XB2)/FORMU)*(XLO*XBO*SIGO(I,J) + TEMPB(I,J))
   22 IF (IP1 .EQ. 0) RETURN
      WRITE(8,3004) UI
 3004 FORMAT (//' UI'/(1X,1P11E11.4))
      WRITE(8,3005) DI
 3005 FORMAT (//' DI'/(1X,1P11E11.4))
      RETURN
      END
      SUBROUTINE LOADER(DONE)
      PARAMETER (LA=31, NUMG=64)
      LOGICAL DONE
      CHARACTER ALF*132
      REAL LAMMIN,LAMMAX
      REAL LAMMIN1,LAMMAX1,GR1,F01
      REAL S1(NUMG,NUMG),T1(NUMG,NUMG),SS1(NUMG,NUMG),TS1(NUMG,NUMG),
     & W1,TAU1
      REAL PTEMP(271)
      DIMENSION S(NUMG,NUMG),T(NUMG,NUMG),SS(NUMG,NUMG),TS(NUMG,NUMG)
      DIMENSION MLAY(LA)
      INTEGER SRW,SRL(LA)
      COMMON/L/ALF,LAMMIN,LAMMAX,GR,F0,NLAY,MAXM,MLAY
      COMMON/HAPKE/HAPKE_B0,HAPKE_B,HAPKE_C,HAPKE_H
      COMMON /PHASEFN/ P(271,LA),THETAP(271)
      DATA SRW/1/

C     Read header records for this wavelength
      READ(10,REC=SRW,IOSTAT=IEND) ALF
      IF(IEND.NE.0) GO TO 1000
      IF(ALF(1:10).EQ.'end of run') GO TO 1000
      IF(SRW+1.EQ.2) READ(10,REC=SRW+1) HAPKE_B0,HAPKE_B,HAPKE_C,HAPKE_H
      READ(10,REC=SRW+2) LAMMIN1,LAMMAX1,GR1,F01,NLAY,MAXM,
     & (MLAY(I),I=1,NLAY)
      LAMMIN=LAMMIN1
      LAMMAX=LAMMAX1
      GR=GR1
      F0=F01

C     Build table of record numbers for first coefficient of each
C     layer.
      SRL(1)=SRW+4
      DO 10 I=2,NLAY
10    SRL(I)=SRL(I-1)+MLAY(I-1)+1

C     Update starting record number for next wavelength
C      LAST=SRL(NLAY)+MLAY(NLAY)-1
      LAST=SRL(NLAY)+MLAY(NLAY)
C      SRW=LAST+1
      SRW=LAST
      RETURN

1000  DONE=.TRUE.
      LAMMIN=0.0
      RETURN

      ENTRY STLOAD(M,L,S,T,SS,TS,W,TAU)
C     Compute record number for this M and L
      N=SRL(L)+M-1
      READ(10,REC=N) W1,TAU1,S1,T1,SS1,TS1
      DO 15 I=1,NUMG
       DO 13 J=1,NUMG
         S(I,J) = S1(I,J)
         T(I,J) = T1(I,J)
         SS(I,J) = SS1(I,J)
         TS(I,J) = TS1(I,J)
13     CONTINUE
15    CONTINUE
      W=W1
      TAU=TAU1
      RETURN

      ENTRY PLOAD(L)
      READ(10,REC=SRL(L)-1) PTEMP
      DO 20 I=1,271
20    P(I,L) = PTEMP(I)
      RETURN
      END
      FUNCTION SSS(AMU,AMU0,DPH,TAU,W,TAUCUM,GR,
     &LEVEL,NBOT,HAPKE_B0,HAPKE_B,HAPKE_C,HAPKE_H)
C     This function evaluates and returns the single scattering S
C     function for a given mu, mu0, delta phi, and LEVEL.  Note that
C     TAU, W, and TAUCUM are arrays giving the optical depth, single
C     scattering albedo, and cumulative optical depth for all layers.

C     Set maximum number of layers:
      PARAMETER (LA=31)
      DIMENSION TAU(LA),W(LA),TAUCUM(LA)

      SINGLE=0.
      CTHETA=-AMU*AMU0+SQRT(1.-AMU**2)*SQRT(1.-AMU0**2)*
     & COS(DPH/57.29577951)
	IF(CTHETA.LT.-1.0) CTHETA=-1.0
	IF(CTHETA.GT.1.0) CTHETA = 1.0
      THETA=ACOS(CTHETA)*57.29577951
      X=1./AMU+1./AMU0

C     Sum contributions from all layers below current LEVEL.
      DO 10 L=LEVEL,NBOT
      IF(TAU(L).GT.0.) THEN
        SINGLE=SINGLE+(1.-EXP(-TAU(L)*X))*PINTER(THETA,L)*W(L)/X*
     &      EXP(-TAUCUM(L)/AMU0-(TAUCUM(L)-TAUCUM(LEVEL))/AMU)
C       write(6,1000)
C    &    AMU,L,(1.-EXP(-TAU(L)*X))*PINTER(THETA,L)*W(L)/X,
C    &    TAU(L),X,THETA,PINTER(THETA,L),W(L)
C1000    format("MU = ",f8.6," L = ",I2," TERM = ",1pg11.3,
C     &  1p5g11.5)
C        pause
      ELSE
        IF(HAPKE_B0.NE.0.0.OR.HAPKE_B.NE.0.0.OR.HAPKE_C.NE.0.0.OR.
     &    HAPKE_H.NE.0.0) THEN
          GAMMA=SQRT(1.0-GR)
          HMU0=(1.0+2.0*AMU0)/(1.0+2.0*GAMMA*AMU0)
          HMU =(1.0+2.0*AMU )/(1.0+2.0*GAMMA*AMU )
          T=180.-THETA
C       B0=HAPKE_S0/(GR*PINTER(180.0,NBOT))
C       B=B0/(1.+1./HAPKE_K*TAN(0.5*T/57.29577951))
          P=PINTER(THETA,NBOT)
          ATTEN=EXP(-TAUCUM(L)/AMU0-(TAUCUM(L)-TAUCUM(LEVEL))/AMU)
          SINGLE = SINGLE+GR*AMU0*AMU/(AMU0+AMU)*(P+HMU0*HMU-1.0)*ATTEN
        ELSE
C     Basic Lambert surface test case (verified)
          GR4MUI = GR*4.0*AMU
          SINGLE = SINGLE+GR4MUI*AMU0*EXP(-TAUCUM(L)/AMU0-(TAUCUM(L)
     &    -TAUCUM(LEVEL))/AMU)
        ENDIF
      ENDIF
10    CONTINUE

      SSS=SINGLE
      RETURN
      END
      FUNCTION SST(AMU,AMU0,DPH,TAU,W,TAUCUM,LEVEL,
     &NBOT)
C     This function evaluates and returns the single scattering T
C     function for a given mu, mu0, delta phi, and LEVEL.  Note that
C     TAU, W, and TAUCUM are arrays giving the optical depth, single
C     scattering albedo, and cumulative optical depth for a layers.

C     Set maximum number of layers:
      PARAMETER (LA=31)
      DIMENSION TAU(LA),W(LA),TAUCUM(LA)

      SST=0.
      CTHETA=+AMU*AMU0+SQRT(1.-AMU**2)*SQRT(1.-AMU0**2)*
     & COS(DPH/57.29577951)
      THETA=ACOS(CTHETA)*57.29577951
      X=1./AMU0-1./AMU

C     Sum contributions from all layers above current LEVEL.
      DO 10 L=1,LEVEL-1
      IF(AMU.NE.AMU0) THEN
        SST=SST+PINTER(THETA,L)*W(L)/X*
     &      (EXP(-TAU(L)/AMU)-EXP(-TAU(L)/AMU0))*
     &       EXP(-TAUCUM(L)/AMU0-(TAUCUM(LEVEL)-TAUCUM(L)-TAU(L))/AMU)
      ELSE
        SST=SST+PINTER(THETA,L)*W(L)*TAU(L)*
     &      EXP(-TAUCUM(L)/AMU0-(TAUCUM(LEVEL)-TAUCUM(L)-TAU(L))/AMU)
      ENDIF
10    CONTINUE

      RETURN
      END
      FUNCTION PINTER(T,L)

C     Interpolate in the phase function for a given layer L for the
C     value of the phase function at angle T (in degrees).

      PARAMETER (LA=31)
      COMMON /PHASEFN/ P(271,LA),THETAP(271)

      CALL LAGRN2(THETAP,P(1,L),271,T/57.29577951,PINTER)
      RETURN
      END
        SUBROUTINE LAGRN2(XARRAY,YARRAY,NPTS,X,FX)
        DIMENSION XARRAY(*),YARRAY(*)
        DIMENSION XT(4), FXT(4), P(4)
C
C  FOUR POINT LAGRANGIAN INTERPOLATION TO OBTAIN FX, GIVEN XARRAY AND
C  YARRAY, AT X.
C
C       SELECT 4 POINTS SURROUNDING REQUIRED VALUE X.
C
        MPTS=NPTS-2
        DO 40 I=3,MPTS
        IF(XARRAY(I).GT.X) GO TO 50
40      CONTINUE
        I=MPTS+1
50      I1=I-2
        DO 60 I=1,4
        XT(I)=XARRAY(I1+I-1)
60      FXT(I)=YARRAY(I1+I-1)
        DO 1 I=1,4
        IF(X.EQ.XT(I)) GO TO 2
    1   CONTINUE
        GO TO 3
    2   FX=FXT(I)
        RETURN
C
C  COMPUTE DENOMINATORS OF LAGRANGIAN COEFFICIENTS
C
    3   DO 5 I=1,4
        PROD = 1.00
        DO 4 J=1,4
        IF(I.EQ.J) GO TO 4
        PROD = PROD*(XT(I)-XT(J))
    4   CONTINUE
        P(I)=PROD
    5   CONTINUE
C
C  COMPUTE GENERAL NUMERATOR
C
        PROD=1.00
        DO 6 I=1,4
        PROD= PROD*(X-XT(I))
    6   CONTINUE
C
C  COMPUTE LAGRANGIAN COEFFICIENTS AND THE INTERPOLATED VALUE
C
        FX=0.00
        DO 7 I=1,4
        XL=PROD/(P(I)*(X-XT(I)))
        FX=FX + XL*FXT(I)
    7   CONTINUE
        RETURN
        END
      SUBROUTINE RENEW(FN)
      CHARACTER*(*) FN
      OPEN(19,FILE=FN,STATUS='UNKNOWN')
      CLOSE(19,STATUS='DELETE')
      RETURN
      END
      SUBROUTINE gauleg(x1,x2,x,w,n)
      INTEGER n
      REAL x1,x2,x(n),w(n)
      PARAMETER (EPS=3.e-14)
      INTEGER i,j,m
      m=(n+1)/2
      xm=0.50*(x2+x1)
      xl=0.50*(x2-x1)
      do 12 i=1,m
        z=cos(3.14159265358979*(i-.25)/(n+.5))
1       continue
          p1=1.0
          p2=0.0
          do 11 j=1,n
            p3=p2
            p2=p1
            p1=((2.00*j-1.0)*z*p2-(j-1.0)*p3)/j
11        continue
          pp=n*(z*p1-p2)/(z*z-1.0)
          z1=z
          z=z1-p1/pp
        if(abs(z-z1).gt.EPS)goto 1
        x(i)=xm-xl*z
        x(n+1-i)=xm+xl*z
        w(i)=2.0*xl/((1.0-z*z)*pp*pp)
        w(n+1-i)=w(i)
12    continue
      return
      END
